#!/usr/bin/python
from abc import ABCMeta, abstractmethod

__author__ = 'nirv'

from boto.cloudtrail import layer1
from chef.utils import json
from CloudServices.Admin.Storage import S3StorageAdmin
from CloudServices.Common.AppConfigMgr import ConfigMgr

class AbstractBaseAudit():
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_logs(self):
        pass


class Audit(AbstractBaseAudit):

    def __init__(self):
        self.__cfg = ConfigMgr()
        self.__conn = layer1.CloudTrailConnection();
        self.__storage = S3StorageAdmin()

    def get_logs(self):
        trails_list = self.__conn.describe_trails()["trailList"]
        logs_list = []
        for trail in trails_list:
            bucket_name = trail["S3BucketName"]
            bucket_prefix = trail["S3KeyPrefix"]
            file_contents_list =  self.__storage.get_all_files(bucket_name, bucket_prefix)
            for file_content in file_contents_list:
                json_content = json.loads(file_content)
                for event in json_content["Records"]:
                    log_entry = self.__get_log_entry_from_json(event)
                    logs_list.append(log_entry)
        return logs_list

    def reset_files_extensions(self):
        trails_list = self.__conn.describe_trails()["trailList"]
        for trail in trails_list:
            bucket_name = trail["S3BucketName"]
            bucket_prefix = trail["S3KeyPrefix"]
            self.__storage.reset_files_extension(bucket_name, bucket_prefix)

    @staticmethod
    def __get_log_entry_from_json(event):
        log_entry = {'timestamp': event["eventTime"]}
        try:
            log_entry['username'] = event["userIdentity"]["userName"]
        except:
            log_entry['username'] = ""
        try:
            log_entry['access_key'] = event["userIdentity"]["accessKeyId"]
        except:
            log_entry['access_key'] = ""
        log_entry['event_name'] = event["eventName"]
        log_entry['event_source'] = event["eventSource"]
        log_entry['source_ip'] = event["sourceIPAddress"]
        log_entry['user_agent'] = event["userAgent"]
        log_entry['region'] = event["awsRegion"]
        log_entry['request_parameters'] = json.dumps(event["requestParameters"])
        log_entry['response'] = json.dumps(event["responseElements"])
        return log_entry


