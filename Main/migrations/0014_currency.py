# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-05-01 10:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0013_delete_currency'),
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='Название')),
                ('symbol', models.CharField(max_length=2, verbose_name='Символ')),
            ],
            options={
                'verbose_name': 'Валюта',
                'verbose_name_plural': 'Валюты',
            },
        ),
    ]