# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_product_main'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='articul',
            field=models.CharField(max_length=30, null=True, verbose_name='Articul', blank=True),
        ),
    ]
