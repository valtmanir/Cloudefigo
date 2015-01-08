#!/usr/bin/python

__author__ = 'nirv'

import gzip
import os
from abc import abstractmethod, ABCMeta

import boto.s3
import boto.s3.bucket
from boto.s3.connection import S3Connection

from CloudServices.Common.Logger import Logger


class AbstractBaseStorageAdmin():
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_all_files(self, storage_name, prefix):
        pass

    @abstractmethod
    def reset_files_extension(self, storage_name, prefix):
         pass


class S3StorageAdmin(AbstractBaseStorageAdmin):

    def __init__(self, region = "us-east-1"):
        self.__s3 = boto.s3.connect_to_region(region)

    def get_all_files(self, storage_name, prefix):
        bucket = self.__s3.get_bucket(storage_name)
        return self.__get_file_contents_list_from_bucket(bucket, prefix, storage_name)

    def reset_files_extension(self, storage_name, prefix):
        bucket = self.__s3.get_bucket(storage_name)
        for key in bucket.list(prefix=prefix):
            if key.name.endswith('-done'):
                new_key_name = key.name.replace('-done','')
                bucket.copy_key(new_key_name=new_key_name, src_bucket_name=storage_name, src_key_name=key.name)
                bucket.delete_key(key.name)

    @staticmethod
    def __get_file_contents_list_from_bucket(bucket, prefix, bucket_name):
        json_files_list = []
        for key in bucket.list(prefix=prefix):
            if key.name.endswith('/') or key.name.endswith('-done'):
                continue
            try:
                new_key_name = "{}-done".format(key.name)
                bucket.copy_key(new_key_name=new_key_name, src_bucket_name=bucket_name, src_key_name=key.name)
                bucket.delete_key(key.name)
                new_key = bucket.get_key(new_key_name)
                new_key.get_contents_to_filename(filename="tmp.json.gz")
                f = gzip.open('tmp.json.gz', 'rb')
                json_files_list.append(f.read())
                f.close()
            except Exception as ex:
                Logger.log("warning", "{} FAILED: {}".format(key.name, ex.message))
        return json_files_list

    def __del__(self):
        try:
            os.remove("tmp.json.gz")
        except:
            pass