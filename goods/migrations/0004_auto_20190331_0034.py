# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2019-03-30 16:34
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0003_auto_20190330_2355'),
    ]

    operations = [
        migrations.RenameField(
            model_name='typeinfo',
            old_name='ttile',
            new_name='ttitle',
        ),
    ]
