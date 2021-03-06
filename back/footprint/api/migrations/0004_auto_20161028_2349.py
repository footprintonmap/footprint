# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-10-28 23:49
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20161028_2338'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2016, 10, 28, 23, 49, 32, 76968, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='image',
            name='modified',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2016, 10, 28, 23, 49, 43, 727461, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='image',
            name='name',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
