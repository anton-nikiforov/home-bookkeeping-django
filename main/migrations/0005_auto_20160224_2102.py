# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-24 21:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20160214_2119'),
    ]

    operations = [
        migrations.AlterField(
            model_name='elements',
            name='category',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, to='main.Category'),
        ),
    ]
