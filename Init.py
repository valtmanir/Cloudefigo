#!/usr/bin/pythonw

__author__ = 'nirv'


from NessusScanner.VulnerabilityAssessment import Scanner
from Common.Exceptions import RemediationException,GenericException
from AWS import S3, EC2
from Common.Logger import Logger

ec2 = EC2.EC2()
bucket = S3.S3()

try:

    encryption_key = "Hello Encryption Key"
    bucket.set_encryption_key(encryption_key)

    nessus = Scanner()
    nessus.run_scan()

    ec2.move_current_instance_to_production_group()
    ec2.post_validation_action()

except RemediationException as re:
    ec2.post_validation_action()
    exit()

except GenericException as ge:
    exit()

except Exception as ex:
    Logger.log("error", ex.message)
    exit()
