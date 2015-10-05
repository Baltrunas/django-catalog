# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_auto_20151002_0706'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['sort', 'name'], 'verbose_name': 'Product', 'verbose_name_plural': 'Products'},
        ),
        migrations.AddField(
            model_name='product',
            name='sort',
            field=models.IntegerField(default=500, null=True, verbose_name='Sort', blank=True),
        ),
    ]
