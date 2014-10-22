#!/usr/bin/python

__author__ = 'nirv'

from Common.AppConfigMgr import ConfigMgr;
from AWS.BotoCfg import BotoCfg
from AWS.EC2 import EC2

config_file_name = "Init.config"

cfgMgr = ConfigMgr();

#botoInit = BotoCfg();
#botoInit.init_credentials_file()

ec2 = EC2("us-east-1", True)
ec2.create_secure_instance("ami-c65be9ae","t1.micro","secure_instance")

# ami-c65be9ae - Ubuntu 14
# ami-cc5be9a4 - Ununtu 12