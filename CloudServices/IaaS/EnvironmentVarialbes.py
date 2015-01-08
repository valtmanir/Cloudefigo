#!/usr/bin/python

__author__ = 'nirv'

import urllib2
import hashlib
import json
from abc import ABCMeta, abstractmethod

from CloudServices.Common.Logger import Logger


class AbstractBaseEnvironmentVariables():
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_current_instance_region(self):
        pass

    @abstractmethod
    def get_current_instance_name(self):
        pass

    @abstractmethod
    def get_current_instance_mac(self):
        pass

    @abstractmethod
    def get_storage_unique_id(prefix):
        pass

    @abstractmethod
    def get_current_instance_profile(self):
        pass

    @abstractmethod
    def get_instance_credentials(self):
        pass


class EnvironmentVariables(AbstractBaseEnvironmentVariables):

    @staticmethod
    def get_current_instance_region():
        return urllib2.urlopen("http://169.254.169.254/latest/meta-data/placement/availability-zone").read()

    @staticmethod
    def get_current_instance_name():
        return urllib2.urlopen("http://169.254.169.254/latest/meta-data/instance-id").read()

    @staticmethod
    def get_current_instance_mac():
        return urllib2.urlopen("http://169.254.169.254/latest/meta-data/mac").read()

    @staticmethod
    def get_storage_unique_id(prefix):
        unique_string_hash = hashlib.sha1(EnvironmentVariables.get_current_instance_name()).hexdigest()
        uppercase_result = "{}-{}".format(prefix, unique_string_hash)
        return uppercase_result.lower()

    @staticmethod
    def get_current_instance_profile():
        response = urllib2.urlopen("http://169.254.169.254/latest/meta-data/iam/info").read()
        parsed_response = json.loads(response)
        profile_arn = parsed_response["InstanceProfileArn"]
        iam_arn_list = profile_arn.split("/")
        return iam_arn_list[len(iam_arn_list) - 1]

    @staticmethod
    def get_instance_credentials():
        try:
            role_name = EnvironmentVariables.get_current_instance_profile();
            creds_url = "http://169.254.169.254/latest/meta-data/iam/security-credentials/{}".format(role_name)
            response = urllib2.urlopen(creds_url).read()
            parsed_response = json.loads(response)
            boto_cfg_access_key_value = parsed_response["AccessKeyId"]
            boto_cfg_secret_key_value = parsed_response["SecretAccessKey"]
            boto_cfg_token = parsed_response["Token"]
            return "{} {} {}".format(boto_cfg_access_key_value, boto_cfg_secret_key_value, boto_cfg_token)
        except:
            Logger.log("error","Cannot get instance credentials from {}".format(creds_url))
            raise