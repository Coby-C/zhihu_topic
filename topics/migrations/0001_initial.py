# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-25 05:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('name', models.CharField(max_length=30, null=True)),
                ('follower_num', models.IntegerField(null=True)),
                ('topic_id', models.IntegerField(primary_key=True, serialize=False)),
                ('is_complete', models.BooleanField(default=False)),
                ('sub_topic', models.ManyToManyField(to='topics.Topic')),
            ],
        ),
    ]
