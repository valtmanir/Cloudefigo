#!/usr/bin/python

__author__ = 'nirv'

import boto
import hashlib
from Common.AppConfigMgr import ConfigMgr
from AWS.EnvironmentVarialbes import EnvronmentVarialbes
from Common.Logger import Logger
from boto.s3.connection import S3Connection

class S3:
    def __init__(self):
        self.__cfg = ConfigMgr()
        self.__bucket_name = self.__cfg.getParameter("AWS", "NamingPrefix")
        self.__bucket_unique_id = EnvronmentVarialbes.get_bucket_unique_id(self.__bucket_name)
        self.__bucket_policy_path = self.__cfg.getParameter("AWS", "BucketPolicyPath")
        self.__current_instance_name = EnvronmentVarialbes.get_current_instance_name()
        credentials = EnvronmentVarialbes.get_instance_credentials().split(" ")
        self.__s3 = S3Connection(aws_access_key_id=credentials[0], aws_secret_access_key=credentials[1], security_token=credentials[2])


    def set_encryption_key(self, encryption_key):
        bucket = self.__s3.create_bucket(self.__bucket_unique_id)
        bucket.set_policy(self.__get_bucket_policy)
        from boto.s3.key import Key
        key_object = Key(bucket)
        key_object.key = "key"
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
        unique_string = "{}{}".format(EnvronmentVarialbes.get_current_instance_mac(), self.__current_instance_name)
        uppercase_result = hashlib.sha512(unique_string).hexdigest()
        return uppercase_result.lower()

    @property
    def __get_bucket_policy(self):
        referer_name = self.__get_referer_unique_id()
        bucket_name = EnvronmentVarialbes.get_bucket_unique_id(self.__bucket_name)
        canonical_user = self.__cfg.getParameter("AWS", "CanonicalUserId")
        with open(self.__bucket_policy_path, "r") as policy_file:
            bucket_policy = policy_file.read().replace('\n', '').replace('\t', '').replace('BUCKETNAME',
                bucket_name).replace('REFERERNAME', referer_name).replace("CANONICALUSER",canonical_user)
            return bucket_policy