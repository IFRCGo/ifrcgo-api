# Generated by Django 2.2.10 on 2020-04-07 09:39

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0053_merge_20200406_1343'),
    ]

    operations = [
        migrations.AddField(
            model_name='action',
            name='category',
            field=models.CharField(choices=[('General', 'General'), ('Health', 'Health')], default='General', max_length=12),
        ),
        migrations.AlterField(
            model_name='action',
            name='field_report_types',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[('EVT', 'Event'), ('EW', 'Early Warning'), ('EPI', 'Epidemic')], max_length=4), default=list, size=None),
        ),
    ]