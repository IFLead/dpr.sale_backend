# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-04-05 22:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0011_auto_20180403_2332'),
    ]

    operations = [
        migrations.CreateModel(
            name='Living_space',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=55, verbose_name='Тип')),
            ],
            options={
                'verbose_name': 'Жилая площадь',
                'verbose_name_plural': 'Жилые площади',
            },
        ),
        migrations.AddField(
            model_name='post',
            name='living_space',
            field=models.ForeignKey(default=django.utils.timezone.now, on_delete=django.db.models.deletion.CASCADE, to='Main.Living_space', verbose_name='Жилая площадь'),
            preserve_default=False,
        ),
    ]