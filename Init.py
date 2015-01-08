#!/usr/bin/python

__author__ = 'nirv'

from Chef.ConfigurationManagement import ChefClient
from NessusScanner.VulnerabilityAssessment import Scanner
from CloudServices.Common.Exceptions import RemediationException,GenericException
from CloudServices.IaaS.Instances import EC2Instance
from CloudServices.Common.Logger import Logger

ec2 = EC2Instance()

try:
    chef_client = ChefClient()
    chef_client.verify_management()

    nessus = Scanner()
    nessus.run_scan()

    ec2.move_current_instance_to_production_group()
    ec2.strict_current_instance_role_permissions()

except RemediationException as re:
    ## ec2.strict_current_instance_role_permissions() ## Depends on the business, it can be added.
    exit()

except GenericException as ge:
    exit()

except Exception as ex:
    Logger.log("error", ex.message)
    exit()
