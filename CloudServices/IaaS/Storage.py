#!/usr/bin/python

__author__ = 'nirv'

import hashlib
from abc import ABCMeta, abstractmethod

from boto.s3.connection import S3Connection

from CloudServices.Common.AppConfigMgr import ConfigMgr
from CloudServices.IaaS.EnvironmentVarialbes import EnvironmentVariables
from CloudServices.Common.Logger import Logger


class AbstractBaseStorage():
    __metaclass__ = ABCMeta

    @abstractmethod
    def generate_and_store_encryption_key(self):
        pass

    @abstractmethod
    def get_encryption_key(self):
        pass


class S3Storage(AbstractBaseStorage):

    def __init__(self):
        self.__cfg = ConfigMgr()
        self.__bucket_name = self.__cfg.get_parameter("Instances", "NamingPrefix")
        self.__bucket_unique_id = EnvironmentVariables.get_storage_unique_id(self.__bucket_name)
        self.__bucket_policy_path = self.__cfg.get_parameter("Instances", "BucketPolicyPath")
        self.__current_instance_name = EnvironmentVariables.get_current_instance_name()
        credentials = EnvironmentVariables.get_instance_credentials().split(" ")
        self.__s3 = S3Connection(aws_access_key_id=credentials[0], aws_secret_access_key=credentials[1], security_token=credentials[2])

    def generate_and_store_encryption_key(self):
        bucket = self.__s3.create_bucket(self.__bucket_unique_id)
        bucket.set_policy(self.__get_bucket_policy)
        from boto.s3.key import Key
        key_object = Key(bucket)
        key_object.key = "key"
        encryption_key = self.__generate_encryption_key()
        key_object.set_contents_from_string(encryption_key, {"Referer": self.__get_referer_unique_id()}, True)
        expires_in_seconds = 1800
        key_object.generate_url(expires_in_seconds)
        Logger.log("info", "Encryption key uploaded to S3 bucket named {}".format(self.__bucket_unique_id))

    def get_encryption_key(self):
        bucket = self.__s3.get_bucket(self.__bucket_unique_id)
        key = bucket.get_key("key", {"Referer": self.__get_referer_unique_id()})
        response = key.get_contents_as_string({"Referer": self.__get_referer_unique_id()})
        Logger.log("info", "Encryption key downloaded")
        return response

    def __get_referer_unique_id(self):
        unique_string = "{}{}".format(EnvironmentVariables.get_current_instance_mac(), self.__current_instance_name)
        uppercase_result = hashlib.sha512(unique_string).hexdigest()
        return uppercase_result.lower()

    def __generate_encryption_key(self):
        from strgen import StringGenerator as SG
        return SG("[\l\d]{100}&[\p]").render()

    @property
    def __get_bucket_policy(self):
        referer_name = self.__get_referer_unique_id()
        bucket_name = EnvironmentVariables.get_storage_unique_id(self.__bucket_name)
        canonical_user = self.__cfg.get_parameter("Instances", "CanonicalUserId")
        with open(self.__bucket_policy_path, "r") as policy_file:
            bucket_policy = policy_file.read().replace('\n', '').replace('\t', '').replace('BUCKETNAME',
                bucket_name).replace('REFERERNAME', referer_name).replace("CANONICALUSER",canonical_user)
            return bucket_policy