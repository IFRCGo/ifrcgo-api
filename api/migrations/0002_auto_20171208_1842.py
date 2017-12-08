# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-08 18:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GDACSEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('eventid', models.CharField(max_length=12)),
                ('title', models.TextField()),
                ('description', models.TextField()),
                ('image', models.URLField(null=True)),
                ('report', models.URLField(null=True)),
                ('publication_date', models.DateTimeField()),
                ('year', models.IntegerField()),
                ('lat', models.FloatField()),
                ('lon', models.FloatField()),
                ('event_type', models.CharField(max_length=16)),
                ('alert_level', models.CharField(max_length=16)),
                ('alert_score', models.CharField(max_length=16, null=True)),
                ('severity', models.TextField()),
                ('severity_unit', models.CharField(max_length=16)),
                ('severity_value', models.CharField(max_length=16)),
                ('population_unit', models.CharField(max_length=16)),
                ('population_value', models.CharField(max_length=16)),
                ('vulnerability', models.IntegerField()),
                ('country_text', models.TextField()),
                ('countries', models.ManyToManyField(to='api.Country')),
            ],
        ),
        migrations.AlterField(
            model_name='event',
            name='dtype',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.DisasterType'),
        ),
    ]
