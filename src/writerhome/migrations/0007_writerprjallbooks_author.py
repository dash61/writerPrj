# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-03 13:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('writerhome', '0006_auto_20170914_1751'),
    ]

    operations = [
        migrations.AddField(
            model_name='writerprjallbooks',
            name='author',
            field=models.CharField(default='Ernst Hempingway', max_length=100),
            preserve_default=False,
        ),
    ]
