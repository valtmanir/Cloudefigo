#!/usr/bin/python
from Common.Logger import Logger
import os

__author__ = 'nirv'

# This class handles the configuration management for this program.
# The configurations taken from a standard XML file
class ConfigMgr:

    config_file_name = "Init.config"

    def __init__(self,):
        import xml.etree.ElementTree as ET
        try:
            self.cfgTree = ET.parse(ConfigMgr.config_file_name)
        except:
            path = os.getcwd()
            Logger.log("error", "Cannot find the configuration file {} in path {}".format(self.config_file_name, path))
            raise
        return

    def getParameter(self, scope, param):
        if self.cfgTree is not None:
            try:
                scopeNode = self.cfgTree.find(scope)
                return scopeNode.find(param).text
            except:
                Logger.log("error",
                                "Cannot find the configuration for the scope {} and parameter {}".format(scope, param))
                raise
        return ""