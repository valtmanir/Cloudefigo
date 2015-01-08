#!/usr/bin/python
from abc import abstractmethod, ABCMeta

__author__ = 'nirv'

import boto
from CloudServices.Common.AppConfigMgr import ConfigMgr
from CloudServices.IaaS.EnvironmentVarialbes import EnvironmentVariables
from boto.iam import IAMConnection


class AbstractBaseIDM():
    __metaclass__ = ABCMeta

    @abstractmethod
    def strict_dynamic_role(self):
        pass


class IAM(AbstractBaseIDM):
    def __init__(self):
        self.__cfg = ConfigMgr()
        self.__iam_strict_policy_path = self.__cfg.get_parameter("Instances", "IAMStrictPolicyPath")
        self.__prefix_name = self.__cfg.get_parameter("Instances", "NamingPrefix")
        credentials = EnvironmentVariables.get_instance_credentials().split(" ")
        self.__conn = IAMConnection(aws_access_key_id=credentials[0], aws_secret_access_key=credentials[1], security_token=credentials[2])
        self.__iam_policy_name = "cloud-sec-policy"

    def strict_dynamic_role(self, iam_role_name):
        with open(self.__iam_strict_policy_path, "r") as policy_file:
            bucket_unique_id = EnvironmentVariables.get_storage_unique_id(self.__prefix_name)
            iam_policy_document = policy_file.read().replace("BUCKETNAME", bucket_unique_id)
            self.__conn.put_role_policy(iam_role_name, self.__iam_policy_name, iam_policy_document)