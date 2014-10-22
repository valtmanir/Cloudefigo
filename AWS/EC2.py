#!/usr/bin/python

__author__ = 'nirv'

import boto.ec2
import time
from Common.AppConfigMgr import ConfigMgr
from AWS.EnvironmentVarialbes import EnvronmentVarialbes
from Common.Logger import Logger
from AWS.IAM import IAM


class EC2:
    def __init__(self, region):
        self.__cfg = ConfigMgr()
        credentials = EnvronmentVarialbes.get_instance_credentials().split(" ")
        self.__conn = boto.ec2.EC2Connection(aws_access_key_id=credentials[0], aws_secret_access_key=credentials[1], security_token=credentials[2])
        self.__conn.region = region
        self.__current_instance_name = EnvronmentVarialbes.get_current_instance_name()


    # <editor-fold desc="Execution during cloud init">

    def move_current_instance_to_remediation_group(self):
        remediation_group_id = self.__cfg.getParameter("AWS", "RemediationSecurityGroupId")
        self.__conn.modify_instance_attribute(self.__current_instance_name,
                                              "groupSet", remediation_group_id)
        Logger.log("info", "This instance moved to the remediation subnet {}".format(remediation_group_id))

    def move_current_instance_to_production_group(self):
        production_group_id = self.__cfg.getParameter("AWS", "ProductionSecurityGroupId")
        instance = self.__get_instance_object_by_instance_id(self.__current_instance_name)
        self.__conn.modify_instance_attribute(self.__current_instance_name,
                                              "groupSet", production_group_id)
        Logger.log("info", "This instance moved to the production subnet {}".format(production_group_id))

    def post_validation_action(self):
        iam = IAM()
        current_role_name = EnvronmentVarialbes.get_current_instance_profile()
        iam.strict_dynamic_role(current_role_name)
        Logger.log("info", "Changed the IAM role to be more strict")

    # </editor-fold>

    # <editor-fold desc="Executed only by the management script">

    def __init__(self, region, is_aws_cli_initiated):
        self.__cfg = ConfigMgr()
        if not is_aws_cli_initiated:
            credentials = EnvronmentVarialbes.get_instance_credentials().split(" ")
            self.__conn = boto.ec2.EC2Connection(aws_access_key_id=credentials[0], aws_secret_access_key=credentials[1], security_token=credentials[2])
            self.__current_instance_name = EnvronmentVarialbes.get_current_instance_name()
        else:
            self.__conn = boto.ec2.connect_to_region(region)
        self.__conn.region = region

    def create_secure_instance(self, ami_id, instance_type, instance_name):
        script_path = self.__cfg.getParameter("AWS", "CloudInitScriptPath")
        production_security_group_id = self.__cfg.getParameter("AWS", "ProductionSecurityGroupId")
        production_subnet_id = self.__cfg.getParameter("AWS", "ProductionSubnetId")
        key_name = self.__cfg.getParameter("AWS", "EC2KeyName")
        with open(script_path, "r") as script_file:
            cloud_init_script = script_file.read()
            iam_role = IAM(True)
            instance_profile = iam_role.create_dynamic_role()
            new_reservation = self.__try_create_instance(ami_id, key_name, instance_profile, instance_type,
                                                         production_subnet_id, production_security_group_id,
                                                         cloud_init_script)
            instance = new_reservation.instances[0]
            self.__conn.create_tags([instance.id], {"Name": instance_name})
            Logger.log("info", "An instance created with id {}".format(instance.id))

    # </editor-fold>

    # TODO remove after testing of new method in EnvironmentVarialbes
    def __get_current_instance_iam_role(self):
        instance = self.__get_instance_object_by_instance_id(self.__current_instance_name)
        iam_arn = instance.instance_profile['arn']
        iam_arn_list = iam_arn.split("/")
        return iam_arn_list[len(iam_arn_list) - 1]

    def __get_instance_object_by_instance_id(self, instance_id):
        reservations = self.__conn.get_all_instances(instance_ids=[instance_id])
        for instance in reservations[0].instances:
            if instance.id == self.__current_instance_name:
                return instance
        return None

    def __try_create_instance(self, ami_id, key_name, profile_name, instance_type, subnet_id,
                              security_group_id, user_data):
        try:
            new_reservation = self.__conn.run_instances(ami_id, key_name=key_name,
                                                        instance_profile_name=profile_name, instance_type=instance_type,
                                                        subnet_id=subnet_id, security_group_ids=[security_group_id],
                                                        user_data=user_data)
            return new_reservation
        except:
            Logger.log("warning", "Could not create instance first time. Waiting another few seconds before retrying")
            time.sleep(30)
            Logger.log("warning", "Retrying to create instance")
            try:
                new_reservation = self.__conn.run_instances(ami_id, key_name=key_name,
                                                            instance_profile_name=profile_name,
                                                            instance_type=instance_type,
                                                            subnet_id=subnet_id, security_group_ids=[security_group_id],
                                                            user_data=user_data)
                return new_reservation
            except Exception as ex:
                message = "Cannot create new instance: {}".format(ex.message)
                Logger.log("error", message)
                raise Exception(message)
