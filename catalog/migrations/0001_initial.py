# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-23 08:07
from __future__ import unicode_literals

import ckeditor_uploader.fields
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('feature', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CatalogCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('title', models.CharField(max_length=255, verbose_name='Категория')),
                ('slug', models.SlugField(default='', max_length=255, verbose_name='Слаг')),
                ('image', models.ImageField(blank=True, default='', upload_to='categories')),
                ('description', ckeditor_uploader.fields.RichTextUploadingField(blank=True, default='', verbose_name='Описание категории')),
                ('active', models.BooleanField(default=True, verbose_name='Вкл/Выкл')),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('feature_set', models.ManyToManyField(to='feature.Set', verbose_name='Набор характеристик')),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='catalog.CatalogCategory')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
            managers=[
                ('_tree_manager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='CatalogComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('text', models.TextField()),
            ],
            options={
                'verbose_name': 'Комментарий',
                'verbose_name_plural': 'Комментарии',
            },
        ),
        migrations.CreateModel(
            name='CatalogCurrency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('title', models.CharField(max_length=100, verbose_name='Название')),
                ('short_title', models.CharField(max_length=5, verbose_name='Сокращение')),
                ('code', models.CharField(max_length=3, verbose_name='Код валюты')),
                ('course', models.DecimalField(decimal_places=4, max_digits=10, verbose_name='Курс')),
                ('is_main', models.BooleanField(verbose_name='Главная')),
            ],
            options={
                'verbose_name': 'Валюта',
                'verbose_name_plural': 'Валюты',
            },
        ),
        migrations.CreateModel(
            name='CatalogImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('image', models.ImageField(blank=True, default='', upload_to='catalog/product_created-%Y-%m-%d', verbose_name='Изображение')),
                ('active', models.BooleanField(default=True, verbose_name='Вкл/Выкл')),
            ],
            options={
                'verbose_name': 'Изображение',
                'verbose_name_plural': 'Изображения',
            },
        ),
        migrations.CreateModel(
            name='CatalogProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('title', models.CharField(max_length=255, verbose_name='Заголовок')),
                ('slug', models.SlugField(default='', max_length=255, verbose_name='Слаг')),
                ('price', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Цена')),
                ('step', models.DecimalField(decimal_places=3, default=1, max_digits=8, verbose_name='Шаг')),
                ('description', models.CharField(blank=True, default='', max_length=170, verbose_name='META DESC')),
                ('text', ckeditor_uploader.fields.RichTextUploadingField(blank=True, default='', verbose_name='Текст поста')),
                ('image', models.ImageField(blank=True, default='', upload_to='catalog/product_created-%Y-%m-%d', verbose_name='Изображение')),
                ('active', models.BooleanField(default=True, verbose_name='Вкл/Выкл')),
                ('category', mptt.fields.TreeForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.CatalogCategory')),
                ('currency', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.CatalogCurrency', verbose_name='Валюта')),
                ('unit', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='feature.Unit', verbose_name='Единица измерения')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
            },
        ),
        migrations.CreateModel(
            name='ProductFeature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('value', models.CharField(blank=True, default=None, max_length=150, null=True, verbose_name='Значение')),
                ('feature', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='feature.Feature', verbose_name='арактеристака')),
                ('product', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.CatalogProduct', verbose_name='Товар')),
                ('unit', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='feature.Unit', verbose_name='Единица измерения')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='catalogimage',
            name='parent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='catalog.CatalogProduct', verbose_name='Изображение'),
        ),
        migrations.AddField(
            model_name='catalogcomment',
            name='parent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parent', to='catalog.CatalogProduct', verbose_name='Товар коментария'),
        ),
    ]
