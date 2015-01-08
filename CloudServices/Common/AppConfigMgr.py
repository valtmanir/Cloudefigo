#!/usr/bin/python
import os

from CloudServices.Common.Logger import Logger

__author__ = 'nirv'

import sys, os
from CloudServices.Common.Exceptions import GenericException


class ConfigMgr:

    def __init__(self,):
        path = self.__get_path()
        import xml.etree.ElementTree as ET
        try:
            self.cfg_tree = ET.parse(path)
        except:
            error_message = "Cannot find the configuration file {}".format(path)
            Logger.log("error", error_message)
            raise GenericException(error_message)

        return

    def get_parameter(self, scope, param):
        if self.cfg_tree is not None:
            try:
                scopeNode = self.cfg_tree.find(scope)
                return scopeNode.find(param).text
            except:
                error_message = "Cannot find the configuration for the scope {} and parameter {}".format(scope, param)
                Logger.log("error", error_message)
                raise GenericException(error_message)
        return ""

    def __get_path(self):
        config_file_name = "Init.config"
        config_folder_name = os.path.dirname(sys.modules[ConfigMgr.__module__].__file__)
        return config_folder_name + "/" + config_file_name
