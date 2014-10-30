#!/bin/bash

# ----------------------
# Install pre-requisites
# ----------------------

# Update the repository to install further packages
add-apt-repository ppa:fkrull/deadsnakes -y
apt-get update

# Python packages
apt-get install python2.7 -y
apt-get install python-pip -y
pip install --upgrade pip setuptools
pip install wheel

# AWS Python SDK
pip install boto

# Chef Python SDK
wget https://pypi.python.org/packages/2.7/P/PyChef/PyChef-0.2.3-py27-none-any.whl
wheel install PyChef-0.2.3-py27-none-any.whl

# Qualysb Python API
pip install qualysapi

# ------------------
# Run the Cloud Init
# ------------------
# python Init.py
echo "Hello World" >> /tmp/data.txt
