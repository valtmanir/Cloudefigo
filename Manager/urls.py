from django.conf.urls import patterns, url
from Manager import views

urlpatterns = patterns('',
    url(r'^$',views.index , name='index'),
    url(r'^events/sync/$', views.sync_events, name='sync'),
    url(r'^events/sync/reset$', views.reset_sync_events, name='sync'),
    url(r'^events/all/$', views.all_events, name='all'),
    url(r'^instances/launch$', views.launch_instance, name='all'),
)