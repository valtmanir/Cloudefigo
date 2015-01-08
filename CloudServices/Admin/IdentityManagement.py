#!/usr/bin/python
from abc import abstractmethod, ABCMeta

__author__ = 'nirv'

import boto
import uuid
from CloudServices.Common.AppConfigMgr import ConfigMgr
from CloudServices.Common.Logger import Logger


class AbstractBaseIDMAdmin():
    __metaclass__ = ABCMeta

    @abstractmethod
    def create_dynamic_role(self):
        pass


class IAMAdmin(AbstractBaseIDMAdmin):
    def __init__(self):
        self.__cfg = ConfigMgr()
        self.__iam_basic_policy_path = self.__cfg.get_parameter("Instances", "IAMBasicPolicyPath")
        self.__prefix_name = self.__cfg.get_parameter("Instances", "NamingPrefix")
        self.__iam_policy_name = "cloud-sec-policy"
        self.__conn = boto.connect_iam()

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
