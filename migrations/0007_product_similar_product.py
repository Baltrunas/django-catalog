# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-15 13:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0006_auto_20160210_1031'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='similar_product',
            field=models.ManyToManyField(blank=True, related_name='_product_similar_product_+', to='catalog.Product', verbose_name='Similar products'),
        ),
    ]
