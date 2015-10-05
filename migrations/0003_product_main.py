# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_auto_20150930_0654'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='main',
            field=models.BooleanField(default=False, verbose_name='Main'),
        ),
    ]
