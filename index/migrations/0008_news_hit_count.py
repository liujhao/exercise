# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-02-01 13:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0007_snatchurls_isdesc'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='hit_count',
            field=models.IntegerField(default=0, verbose_name='点击数'),
        ),
    ]
