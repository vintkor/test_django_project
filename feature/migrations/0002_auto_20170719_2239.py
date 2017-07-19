# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-19 19:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('feature', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feature',
            name='unit',
        ),
        migrations.AddField(
            model_name='unit',
            name='feature',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='feature.Feature', verbose_name='Характеристика'),
        ),
    ]
