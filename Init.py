#!/usr/bin/python

__author__ = 'nirv'

from Chef.ConfigurationManagement import ChefClient
from NessusScanner.VulnerabilityAssessment import Scanner
from Common.Exceptions import RemediationException,GenericException
from AWS.EC2 import EC2
from Common.Logger import Logger

ec2 = EC2()

try:
    chef_client = ChefClient()
    chef_client.verify_management()

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
