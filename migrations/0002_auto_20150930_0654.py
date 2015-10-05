# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['real_order', 'name'], 'verbose_name': 'Category', 'verbose_name_plural': 'Categories'},
        ),
        migrations.AddField(
            model_name='product',
            name='guid',
            field=models.CharField(max_length=37, null=True, verbose_name='GUID', blank=True),
        ),
    ]
