# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-10-28 21:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]
