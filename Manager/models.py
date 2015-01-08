from django.db import models
import json


class Event(models.Model):
    timestamp = models.CharField(max_length=20)
    username = models.CharField(max_length=200)
    access_key = models.CharField(max_length=50)
    event_name = models.CharField(max_length=50)
    event_source = models.CharField(max_length=50)
    source_ip = models.CharField(max_length=15)
    user_agent = models.CharField(max_length=70)
    region = models.CharField(max_length=15)
    request_parameters = models.CharField(max_length=800)
    response = models.CharField(max_length=800)

    def set_by_key_value_list(self, key_value_list = None):
        if key_value_list is not None:
            self.timestamp = key_value_list['timestamp']
            self.username = key_value_list['username']
            self.access_key = key_value_list['access_key']
            self.event_name = key_value_list['event_name']
            self.event_source = key_value_list['event_source']
            self.source_ip = key_value_list['source_ip']
            self.user_agent = key_value_list['user_agent']
            self.region = key_value_list['region']
            self.request_parameters = key_value_list['request_parameters']
            self.response = key_value_list['response']

    def __unicode__(self):
        return json.dumps(self.get_key_value_list())


    def get_key_value_list(self):
        key_value_list = {'timestamp': self.timestamp, 'username': self.username, 'access_key': self.access_key,
                          'event_name': self.event_name, 'event_source': self.event_source, 'source_ip': self.source_ip,
                          'user_agent': self.user_agent, 'region': self.region,
                          'request_parameters': self.request_parameters, 'response': self.response}
        return key_value_list




