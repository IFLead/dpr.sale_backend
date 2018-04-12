# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-04-12 21:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0012_auto_20180405_2247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='district',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Main.District', verbose_name='Район'),
        ),
        migrations.AlterField(
            model_name='post',
            name='living_space',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Main.Living_space', verbose_name='Жилая площадь'),
        ),
        migrations.AlterField(
            model_name='post',
            name='material',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Main.Material', verbose_name='Материал'),
        ),
        migrations.AlterField(
            model_name='post',
            name='state',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Main.State', verbose_name='Состояние'),
        ),
        migrations.AlterField(
            model_name='post',
            name='storeys',
            field=models.PositiveSmallIntegerField(default=1, null=True, verbose_name='Этажность здания'),
        ),
        migrations.AlterField(
            model_name='post',
            name='window',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Main.Window', verbose_name='Окно'),
        ),
    ]
