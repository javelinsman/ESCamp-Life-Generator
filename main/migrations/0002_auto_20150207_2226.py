# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='story',
            name='is_event',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='transition',
            name='is_buff',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
