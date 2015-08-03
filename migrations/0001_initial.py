# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import apps.catalog.models
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('public', models.BooleanField(default=True, verbose_name='Public')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('name', models.CharField(max_length=128, verbose_name='Name')),
                ('slug', models.SlugField(help_text='A slug is the part of a URL which identifies a page using human-readable keywords', max_length=128, verbose_name='Slug')),
                ('logo', models.FileField(upload_to=apps.catalog.models.brand_upload, null=True, verbose_name='Logo', blank=True)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Brand',
                'verbose_name_plural': 'Brands',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('public', models.BooleanField(default=True, verbose_name='Public')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('name', models.CharField(max_length=128, verbose_name='Name')),
                ('slug', models.SlugField(help_text='A slug is the part of a URL which identifies a page using human-readable keywords', max_length=128, verbose_name='Slug')),
                ('cover', models.FileField(upload_to=apps.catalog.models.category_cover_upload, null=True, verbose_name='Cover', blank=True)),
                ('icon', models.FileField(upload_to=apps.catalog.models.category_icon_upload, null=True, verbose_name='Icon', blank=True)),
                ('level', models.IntegerField(default=0, editable=False)),
                ('order', models.IntegerField(default=500, null=True, blank=True)),
                ('real_order', models.IntegerField(default=500, null=True, editable=False, blank=True)),
                ('childs_count', models.IntegerField(default=0, null=True, editable=False, blank=True)),
                ('products_count', models.IntegerField(default=0, null=True, editable=False, blank=True)),
                ('products_total_count', models.IntegerField(default=0, null=True, editable=False, blank=True)),
                ('url', models.CharField(verbose_name='URL', max_length=1024, null=True, editable=False, blank=True)),
                ('parent', models.ForeignKey(related_name='childs', verbose_name='Parent', blank=True, to='catalog.Category', null=True)),
            ],
            options={
                'ordering': ['real_order'],
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('public', models.BooleanField(default=True, verbose_name='Public')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('name', models.CharField(max_length=128, null=True, verbose_name='Name', blank=True)),
                ('image', models.FileField(upload_to=apps.catalog.models.image_upload, verbose_name='Image')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Image',
                'verbose_name_plural': 'Images',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('public', models.BooleanField(default=True, verbose_name='Public')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('sync_id', models.IntegerField(verbose_name='Sync ID', null=True, editable=False, blank=True)),
                ('barcode', models.CharField(max_length=40, null=True, verbose_name='Barcode', blank=True)),
                ('name', models.CharField(max_length=500, verbose_name='Name')),
                ('cover', models.FileField(upload_to=apps.catalog.models.product_upload, null=True, verbose_name='Image', blank=True)),
                ('description', models.TextField(null=True, verbose_name='Description', blank=True)),
                ('articul', models.CharField(max_length=30, verbose_name='Articul')),
                ('retail_price', models.DecimalField(default=Decimal('0.0000'), verbose_name='Retail Price', max_digits=16, decimal_places=4)),
                ('wholesale_price', models.DecimalField(decimal_places=4, default=Decimal('0.0000'), max_digits=16, blank=True, null=True, verbose_name='Wholesale Price')),
                ('retail_price_with_discount', models.DecimalField(decimal_places=4, default=Decimal('0.0000'), max_digits=16, blank=True, null=True, verbose_name='Retail Price With Discount')),
                ('min_quantity_for_order', models.IntegerField(default=0, verbose_name='Min Quantity For Order')),
                ('warehouse_quantity', models.IntegerField(default=0, verbose_name='Warehouse Quantity')),
                ('height', models.IntegerField(null=True, verbose_name='Height', blank=True)),
                ('width', models.IntegerField(null=True, verbose_name='Width', blank=True)),
                ('size', models.CharField(max_length=20, null=True, verbose_name='The Size', blank=True)),
                ('color', models.CharField(max_length=50, null=True, verbose_name='Color', blank=True)),
                ('material', models.CharField(max_length=200, null=True, verbose_name='Material', blank=True)),
                ('sex', models.SmallIntegerField(default=0, verbose_name='Sex', choices=[(0, 'Undefined'), (1, 'Man'), (2, 'Women'), (3, 'Boy'), (4, 'Girl'), (5, 'Unisex')])),
                ('season', models.CharField(max_length=100, null=True, verbose_name='Season', blank=True)),
                ('age', models.CharField(max_length=256, null=True, verbose_name='Age', blank=True)),
                ('deleted', models.BooleanField(default=False, verbose_name='Deleted')),
                ('brand', models.ForeignKey(verbose_name='Brand', blank=True, to='catalog.Brand', null=True)),
                ('category', models.ForeignKey(related_name='products', verbose_name='Category', blank=True, to='catalog.Category', null=True)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
            },
        ),
        migrations.AddField(
            model_name='image',
            name='product',
            field=models.ForeignKey(related_name='images', verbose_name='Product', to='catalog.Product'),
        ),
    ]
