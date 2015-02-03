import json
from django.http import HttpResponse
from Manager.models import Event
from CloudServices.Admin.Instances import EC2InstanceAdmin
from CloudServices.Admin.CloudTrail import Audit
from Chef.ConfigurationManagement import ChefClient


def index(request):
    return HttpResponse('{"Status": "Management API is Alive!"}', content_type="application/json")


def sync_events(request):
    audit = Audit()
    logs_list = audit.get_logs()
    for log_entry in logs_list:
        log = Event()
        log.set_by_key_value_list(log_entry)
        log.save()
    return HttpResponse('{"Status": "Done"}', content_type="application/json")


def reset_sync_events(request):
    audit = Audit()
    audit.reset_files_extensions()
    return HttpResponse('{"Status": "Done"}', content_type="application/json")


def all_events(request):
    all_events_in_db = Event.objects.order_by('-timestamp')
    events_json_list = []
    for event in all_events_in_db:
        events_json_list.append(event.get_key_value_list())
    json_element = {'logs': events_json_list}
    return HttpResponse(json.dumps(json_element), content_type="application/json")

def launch_instance(request):
    launcher = EC2InstanceAdmin(region = "us-east-1")
    status = launcher.create_secure_instance("ami-c65be9ae","t1.micro","Secure Instance") # ami-c65be9ae is Ubuntu 14
    return HttpResponse('{"Status": "OK"}', content_type="application/json")


def get_unmanaged_servers(request):
    launcher = EC2InstanceAdmin(region = "us-east-1")
    chef = ChefClient()
    iaas_instance_names = launcher.get_all_running_instance_names()
    chef_nodes = chef.get_all_nodes()
    unmanaged_nodes = []
    for ec2_instance in iaas_instance_names:
       if ec2_instance not in chef_nodes:
             unmanaged_nodes.append(ec2_instance)
    response_key_value = {"Unmanaged" : unmanaged_nodes}
    return HttpResponse(json.dumps(response_key_value), content_type="application/json")
