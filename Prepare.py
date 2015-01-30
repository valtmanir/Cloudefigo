#!/usr/bin/python

__author__ = 'nirv'

from CloudServices.IaaS.Storage import S3Storage
from CloudServices.IaaS.Instances import EC2Instance
from CloudServices.Common.Logger import Logger
import sys

try:
    ec2 = EC2Instance()
    ec2.attach_new_storage_to_current_instance()

    bucket = S3Storage()
    if len(sys.argv) > 1:
        bucket.generate_and_store_encryption_key()

    with open("key","a+") as key_file:
        key_file.write(bucket.get_encryption_key())
        key_file.close();

except Exception as ex:
    Logger.log("error", ex.message)
    exit()
