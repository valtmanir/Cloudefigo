#!/usr/bin/python

__author__ = 'nirv'

import logging

class Logger:

    logger_initiated = False
    logger = None

    @classmethod
    def init(cls):
        import socket
        hostname = socket.gethostname()
        cls.logger = logging.getLogger()
        cls.logger.setLevel(logging.INFO)
        handler = logging.FileHandler("init.log")
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(levelname)s, {}, %(asctime)s, %(message)s'.format(hostname),
                                      '%m/%d/%Y %I:%M:%S %p')
        handler.setFormatter(formatter)
        cls.logger.addHandler(handler)
        cls.logger_initiated = True

    @classmethod
    def log(cls, log_type, message):
        if cls.logger_initiated is False:
            cls.init();
        print "{}: {}".format(log_type, message)
        if log_type.upper() == "CRITICAL":
            cls.logger.critical(message)
        elif log_type.upper() == "ERROR":
            cls.logger.error(message)
        elif log_type.upper() == "WARNING":
            cls.logger.warning(message)
        else:
            cls.logger.info(message)