#!/usr/bin/python

# __author__ = 'nirv'

from CloudServices.Common.Logger import Logger


class RemediationException(Exception):

    def __init__(self, message):
        super(RemediationException, self).__init__(message)
        Logger.log("critical", message)

class GenericException(Exception):

    def __init__(self, message):
        super(GenericException, self).__init__(message)
        Logger.log("error", message)