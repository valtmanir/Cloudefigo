from django.contrib import admin
from Manager.models import Event


class EventAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'username', 'access_key', 'event_name', 'event_source', 'source_ip', 'user_agent',
                    'region', 'request_parameters', 'response')
    search_fields = ['username', 'access_key', 'event_name', 'event_source', 'source_ip', 'user_agent',
                     'region', 'request_parameters', 'response']


admin.site.register(Event, EventAdmin)