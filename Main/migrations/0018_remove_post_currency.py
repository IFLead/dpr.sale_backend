# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-05-01 12:49
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0017_auto_20180501_1249'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='currency',
        ),
    ]
