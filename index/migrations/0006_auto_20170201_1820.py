# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-02-01 10:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0005_auto_20170201_1758'),
    ]

    operations = [
        migrations.AlterField(
            model_name='snatchurls',
            name='last_date',
            field=models.DateTimeField(null=True, verbose_name='最后抓取时间'),
        ),
    ]
