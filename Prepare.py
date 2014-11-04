#!/usr/bin/python

__author__ = 'nirv'

from AWS.S3 import S3
from AWS.EC2 import EC2
from Common.Logger import Logger
import sys

try:
    ec2 = EC2()
    ec2.create_volume()

    bucket = S3()
    if len(sys.argv) > 1:
        bucket.set_encryption_key()

    with open("key","a+") as key_file:
        key_file.write(bucket.get_encryption_key())
        key_file.close();

except Exception as ex:
    Logger.log("error", ex.message)
    exit()
