__author__ = 'nirv'

from CloudServices.Admin.CloudTrail import Audit

audit = Audit()
print audit.get_logs()