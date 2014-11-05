#!/usr/bin/python

__author__ = 'nirv'

from chef import Node, ChefAPI
from Common.AppConfigMgr import ConfigMgr
from Common.Logger import Logger
from Common.Exceptions import RemediationException


class ChefClient:

    def __init__(self):
        cfg = ConfigMgr()
        url = cfg.getParameter("Chef","ServerURL")
        key_path = cfg.getParameter("Chef","KeyFilePath")
        client_name = cfg.getParameter("Chef","ValidationClientName")
        self.__chef_client = ChefAPI(url,key_path,client_name)

    def verify_management(self):
        node = Node(self.__get_hostname())
        if node.exists:
            Logger.log("info", "The server is managed by Chef")
            return
        raise RemediationException("The server is not managed by Chef. Please make sure it is managed before promoting to production.")

    def get_all_nodes(self):
        return Node.list().names

    def __get_hostname(self):
        import socket
        return socket.gethostname()