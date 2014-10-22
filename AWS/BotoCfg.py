#!/usr/bin/python

__author__ = 'nirv'

import os
import urllib2
import json
from Common.Logger import Logger
from Common.AppConfigMgr import ConfigMgr
from AWS.EnvironmentVarialbes import EnvronmentVarialbes

class BotoCfg:

    def __init__(self):
        self.app_cfg = ConfigMgr()
        self.scope_name = "AWS"
        self.boto_cfg_creds_name = "Credentials"
        self.boto_cfg_access_key_name = "aws_access_key_id"
        self.boto_cfg_access_key_value = None
        self.boto_cfg_secret_key_name = "aws_secret_access_key"
        self.boto_cfg_secret_key_value = None
        self.boto_cfg_path = "{}/.boto".format(os.path.expanduser('~'))
        return

    def __get_instance_credentials(self):
        try:
            role_name = EnvronmentVarialbes.get_current_instance_profile();
            creds_url = "http://169.254.169.254/latest/meta-data/iam/security-credentials/{}".format(role_name)
            response = urllib2.urlopen(creds_url).read()
            parsed_response = json.loads(response)
            self.boto_cfg_access_key_value = parsed_response["AccessKeyId"]
            self.boto_cfg_secret_key_value = parsed_response["SecretAccessKey"]
        except:
            Logger.log("error","Cannot get instance credentials from {}".format(creds_url))
            raise

    def init_credentials_file(self):
        #self.boto_cfg_access_key_value = "AKIAIPYLAZMX3QABKLIA"
        #self.boto_cfg_secret_key_value = "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"
        self.__get_instance_credentials()
        with open(self.boto_cfg_path,"a+") as configfile:
            configfile.write("[{}]\n".format(self.boto_cfg_creds_name))
            configfile.write("{} = {}\n".format(self.boto_cfg_access_key_name, self.boto_cfg_access_key_value))
            configfile.write("{} = {}\n".format(self.boto_cfg_secret_key_name, self.boto_cfg_secret_key_value))
            configfile.close();

    def __del__(self):
        os.remove(self.boto_cfg_path)


