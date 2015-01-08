#!/usr/bin/python

__author__ = 'nirv'

import time
from abc import abstractmethod, ABCMeta

import boto.ec2

from CloudServices.Common.AppConfigMgr import ConfigMgr
from CloudServices.IaaS.EnvironmentVarialbes import EnvironmentVariables
from CloudServices.Common.Logger import Logger
from CloudServices.IaaS.IdentityManagement import IAM


class AbstractBaseInstance():
    __metaclass__ = ABCMeta

    @abstractmethod
    def attach_new_storage_to_current_instance(self):
        pass

    @abstractmethod
    def move_current_instance_to_production_group(self):
        pass

    @abstractmethod
    def strict_current_instance_role_permissions(self):
        pass


class EC2Instance(AbstractBaseInstance):

    def __init__(self):
        self.__cfg = ConfigMgr()
        credentials = EnvironmentVariables.get_instance_credentials().split(" ")
        self.__conn = boto.ec2.EC2Connection(aws_access_key_id=credentials[0], aws_secret_access_key=credentials[1], security_token=credentials[2])
        self.__conn.region = EnvironmentVariables.get_current_instance_region()
        self.__current_instance_name = EnvironmentVariables.get_current_instance_name()

    def attach_new_storage_to_current_instance(self):
        inst = self.get_instance_object_by_instance_id(self.__current_instance_name)
        vol = self.__conn.create_volume(1,self.__conn.region)
        time.sleep(30)
        curr_vol = self.__conn.get_all_volumes([vol.id])[0]
        while curr_vol.status != 'available':
            time.sleep(10)
            Logger.logger("info", "pending to make volume available")
        self.__conn.attach_volume (vol.id, inst.id, "/dev/sdf")
        Logger.log("info", "The volume {} attached to this instance".format(vol.id))

    def move_current_instance_to_production_group(self):
        production_group_id = self.__cfg.get_parameter("Instances", "ProductionSecurityGroupId")
        instance = self.get_instance_object_by_instance_id(self.__current_instance_name)
        self.__conn.modify_instance_attribute(self.__current_instance_name,
                                              "groupSet", [production_group_id])
        Logger.log("info", "This instance moved to the production subnet {}".format(production_group_id))

    def strict_current_instance_role_permissions(self):
        iam = IAM()
        current_role_name = EnvironmentVariables.get_current_instance_profile()
        iam.strict_dynamic_role(current_role_name)
        Logger.log("info", "Changed the IAM role to be more strict")

    def get_instance_object_by_instance_id(self, instance_id):
        reservations = self.__conn.get_all_instances(instance_ids=[instance_id])
        for instance in reservations[0].instances:
            if instance.id == self.__current_instance_name:
                return instance
        return None

