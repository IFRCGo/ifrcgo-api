# Generated by Django 2.2.20 on 2021-06-15 09:20

import api.models
from django.db import migrations, models
import django.db.models.deletion
import enumfields.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0129_appealhistory_fill'),
    ]

    operations = [
        migrations.AddField(
            model_name='appealhistory',
            name='dtype',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.DisasterType', verbose_name='disaster type'),
        ),
        migrations.AddField(
            model_name='appealhistory',
            name='needs_confirmation',
            field=models.BooleanField(default=False, verbose_name='needs confirmation?'),
        ),
        migrations.AddField(
            model_name='appealhistory',
            name='status',
            field=enumfields.fields.EnumIntegerField(default=0, enum=api.models.AppealStatus, verbose_name='status'),
        ),
        migrations.AddField(
            model_name='appealhistory',
            name='code',
            field=models.CharField(max_length=20, null=True, verbose_name='code'),
        ),
    ]
