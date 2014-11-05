#!/usr/bin/python

__author__ = 'nirv'

from Chef.ConfigurationManagement import ChefClient
from AWS.EC2 import EC2

def get_menu():
    return ("\n----- Secure Cloud Management Console -----\n"
            "1. Launch secure instance\n"
            "2. Locate not managed instances\n"
            "3. Exit\n"
            "Your choise: ")

ec2 = EC2(False, "us-east-1")
chef = ChefClient()

while True:
    response = raw_input(get_menu())
    if response == '1':
        ec2.create_secure_instance("ami-c65be9ae","t1.micro","Secure Instance") # ami-c65be9ae is Ubuntu 14
    elif response == '2':
        ec2_instances = ec2.get_all_running_instance_names()
        chef_nodes = chef.get_all_nodes()
        print "Not managed nodes list: "
        for ec2_instance in ec2_instances:
            if ec2_instance not in chef_nodes:
                print ec2_instance
    else:
        exit()