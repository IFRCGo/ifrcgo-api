# Generated by Django 2.2.13 on 2020-07-29 09:51

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0079_auto_20200728_0920'),
    ]

    operations = [
        migrations.AddField(
            model_name='region',
            name='bbox',
            field=django.contrib.gis.db.models.fields.PolygonField(blank=True, null=True, srid=4326),
        ),
    ]