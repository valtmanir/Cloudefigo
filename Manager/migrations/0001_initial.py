# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.CharField(max_length=20)),
                ('username', models.CharField(max_length=200)),
                ('access_key', models.CharField(max_length=50)),
                ('event_name', models.CharField(max_length=50)),
                ('event_source', models.CharField(max_length=50)),
                ('source_ip', models.CharField(max_length=15)),
                ('user_agent', models.CharField(max_length=70)),
                ('region', models.CharField(max_length=15)),
                ('request_parameters', models.CharField(max_length=800)),
                ('response', models.CharField(max_length=800)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
