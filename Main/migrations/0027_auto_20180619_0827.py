# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-06-19 08:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('Main', '0026_merge_20180527_1610'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='treecategory',
            options={'verbose_name': 'Тип недвижимости', 'verbose_name_plural': 'Типы недвижимости'},
        ),
        migrations.AlterField(
            model_name='post',
            name='address',
            field=models.TextField(blank=True, help_text='Не отображается на сайте', null=True, verbose_name='Адрес'),
        ),
        migrations.AlterField(
            model_name='post',
            name='category_tree',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                    to='Main.TreeCategory', verbose_name='Тип недвижимости'),
        ),
        migrations.AlterField(
            model_name='post',
            name='closed',
            field=models.BooleanField(default=False, verbose_name='Открыт'),
        ),
        migrations.AlterField(
            model_name='post',
            name='contacts',
            field=models.TextField(blank=True, help_text='Не отображается на сайте', null=True,
                                   verbose_name='Контакты'),
        ),
        migrations.AlterField(
            model_name='post',
            name='material',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                    to='Main.Material', verbose_name='Материал'),
        ),
        migrations.AlterField(
            model_name='post',
            name='private_description',
            field=models.TextField(blank=True, help_text='Не отображается на сайте', null=True,
                                   verbose_name='Комментарии от риелтора'),
        ),
        migrations.AlterField(
            model_name='post',
            name='storeys',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Этажность здания'),
        ),
    ]
