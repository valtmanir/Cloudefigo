#!/usr/bin/python

__author__ = 'nirv'


from AWS.S3 import S3
from AWS.EC2 import EC2
from Common.Logger import Logger

s3 = S3()
encryption_key = "Hello Encryption Key"
s3.set_encryption_key(encryption_key)
Logger.log("info", "The encryption key posted and received from S3")


ec2 = EC2("us-east-1")

# This should run only if the instance does NOT comply with the security policy
ec2.move_current_instance_to_remediation_group()
Logger.log("info", "Instance Moved to remediation security group")
ec2.move_current_instance_to_production_group()
Logger.log("info", "Instance Moved to production security group")



# This should run only of the instance comply with the security policy
ec2.post_validation_action()

