#!/usr/bin/python

__author__ = 'nirv'

from AWS.EC2 import EC2

ec2 = EC2(False, "us-east-1")
ec2.create_secure_instance("ami-c65be9ae","t1.micro","secure_scanned_instance")

# ami-c65be9ae is Ubuntu 14