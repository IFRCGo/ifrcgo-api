# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2017-12-12 19:26
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20171212_0241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fieldreport',
            name='originator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user', to=settings.AUTH_USER_MODEL),
        ),
    ]
