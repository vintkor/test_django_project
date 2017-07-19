# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-19 19:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('feature', '0001_initial'),
        ('catalog', '0003_auto_20170719_2158'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductFeature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('value', models.CharField(default=None, max_length=150, verbose_name='Значение')),
                ('feature', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='feature.Feature', verbose_name='арактеристака')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='catalogproduct',
            name='feature',
        ),
        migrations.AddField(
            model_name='productfeature',
            name='product',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.CatalogProduct', verbose_name='Товар'),
        ),
        migrations.AddField(
            model_name='productfeature',
            name='unit',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='feature.Unit', verbose_name='Единица измерения'),
        ),
    ]
