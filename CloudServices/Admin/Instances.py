#!/usr/bin/python

__author__ = 'nirv'

import time
from abc import abstractmethod, ABCMeta

import boto.ec2

from CloudServices.Common.AppConfigMgr import ConfigMgr
from CloudServices.Common.Exceptions import GenericException
from CloudServices.Admin.IdentityManagement import IAMAdmin
from CloudServices.Common.Logger import Logger


class AbstractBaseInstanceAdmin():
    __metaclass__ = ABCMeta

    @abstractmethod
    def create_secure_instance(self, image_id, instance_type, instance_name):
        pass

    @abstractmethod
    def get_all_running_instance_names(self):
        pass


class EC2InstanceAdmin(AbstractBaseInstanceAdmin):

    def __init__(self, region = None):
        self.__cfg = ConfigMgr()
        self.__conn = boto.ec2.connect_to_region(region)

    def create_secure_instance(self, image_id, instance_type, instance_name):
        script_path = self.__cfg.get_parameter("Instances", "CloudInitScriptPath")
        production_security_group_id = self.__cfg.get_parameter("Instances", "RemediationSecurityGroupId")
        production_subnet_id = self.__cfg.get_parameter("Instances", "ProductionSubnetId")
        key_name = self.__cfg.get_parameter("Instances", "EC2KeyName")
        with open(script_path, "r") as script_file:
            cloud_init_script = script_file.read()
            iam_role = IAMAdmin()
            instance_profile = iam_role.create_dynamic_role()
            new_reservation = self.__try_create_instance(image_id, key_name, instance_profile, instance_type,
                                                         production_subnet_id, production_security_group_id,
                                                         cloud_init_script)
            instance = new_reservation.instances[0]
            self.__conn.create_tags([instance.id], {"Name": instance_name})
            message = "An instance created with id {}".format(instance.id)
            Logger.log("info", message)
            return message

    def get_all_running_instance_names(self):
        instances_list = []
        instances = self.__conn.get_all_instances()
        for instance in instances:
            if instance.instances[0].state == "running":
                instance_hostname =  instance.instances[0].private_dns_name.split('.')[0]
                instances_list.append(instance_hostname)
        return instances_list

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
                raise GenericException(message)
