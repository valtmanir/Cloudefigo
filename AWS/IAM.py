#!/usr/bin/python

__author__ = 'nirv'


import boto
import uuid
from Common.AppConfigMgr import ConfigMgr
from AWS.EnvironmentVarialbes import EnvronmentVarialbes
from Common.Logger import Logger
from boto.iam import IAMConnection



class IAM:
    def __init__(self, is_initiated_by_cloud_init = True):
        self.__cfg = ConfigMgr()
        self.__iam_basic_policy_path = self.__cfg.getParameter("AWS", "IAMBasicPolicyPath")
        self.__iam__strict_policy_path = self.__cfg.getParameter("AWS", "IAMStrictPolicyPath")
        self.__prefix_name = self.__cfg.getParameter("AWS", "NamingPrefix")
        if is_initiated_by_cloud_init:
            credentials = EnvronmentVarialbes.get_instance_credentials().split(" ")
            self.__conn = IAMConnection(aws_access_key_id=credentials[0], aws_secret_access_key=credentials[1], security_token=credentials[2])
        else:
            self.__conn = boto.connect_iam()
        self.__iam_policy_name = "cloud-sec-policy"

    # <editor-fold desc="Executed only by the management script">

    def create_dynamic_role(self):
        random_id = uuid.uuid4().get_hex()
        with open(self.__iam_basic_policy_path, "r") as policy_file:
            iam_role_name = "{}-{}".format(self.__prefix_name, random_id)
            iam_policy_document = policy_file.read().replace("BUCKETNAME", "{}*".format(self.__prefix_name))
            self.__conn.create_role(iam_role_name)
            self.__conn.create_instance_profile(iam_role_name)
            self.__conn.add_role_to_instance_profile(iam_role_name, iam_role_name)
            self.__conn.put_role_policy(iam_role_name, self.__iam_policy_name, iam_policy_document)
            Logger.log("info", "Created a dynamic role named {}".format(iam_role_name))
            return iam_role_name

    # </editor-fold>

    def strict_dynamic_role(self, iam_role_name):
        with open(self.__iam__strict_policy_path, "r") as policy_file:
            bucket_unique_id = EnvronmentVarialbes.get_bucket_unique_id(self.__prefix_name)
            iam_policy_document = policy_file.read().replace("BUCKETNAME", bucket_unique_id)
            self.__conn.put_role_policy(iam_role_name, self.__iam_policy_name, iam_policy_document)