# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-05-01 15:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0017_treecategory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='treecategory',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]
