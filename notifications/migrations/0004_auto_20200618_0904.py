# Generated by Django 2.2.13 on 2020-06-18 09:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import enumfields.fields
import notifications.models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0003_notificationguid'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='subscription',
            options={'verbose_name': 'Subscription', 'verbose_name_plural': 'Subscriptions'},
        ),
        migrations.AlterModelOptions(
            name='surgealert',
            options={'ordering': ['-created_at'], 'verbose_name': 'Surge Alert', 'verbose_name_plural': 'Surge Alerts'},
        ),
        migrations.AlterField(
            model_name='notificationguid',
            name='api_guid',
            field=models.CharField(help_text='Can be used to do a GET request to check on the email sender API side.', max_length=200),
        ),
        migrations.AlterField(
            model_name='notificationguid',
            name='email_type',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='notificationguid',
            name='to_list',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.Country', verbose_name='country'),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='dtype',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.DisasterType', verbose_name='disaster type'),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='event',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.Event', verbose_name='event'),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='lookup_id',
            field=models.CharField(blank=True, editable=False, max_length=20, null=True, verbose_name='lookup id'),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='region',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.Region', verbose_name='region'),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='rtype',
            field=enumfields.fields.EnumIntegerField(default=0, enum=notifications.models.RecordType, verbose_name='record type'),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='stype',
            field=enumfields.fields.EnumIntegerField(default=0, enum=notifications.models.SubscriptionType, verbose_name='subscription type'),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscription', to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
        migrations.AlterField(
            model_name='surgealert',
            name='atype',
            field=enumfields.fields.EnumIntegerField(default=0, enum=notifications.models.SurgeAlertType, verbose_name='alert type'),
        ),
        migrations.AlterField(
            model_name='surgealert',
            name='category',
            field=enumfields.fields.EnumIntegerField(default=0, enum=notifications.models.SurgeAlertCategory, verbose_name='category'),
        ),
        migrations.AlterField(
            model_name='surgealert',
            name='created_at',
            field=models.DateTimeField(verbose_name='created at'),
        ),
        migrations.AlterField(
            model_name='surgealert',
            name='deployment_needed',
            field=models.BooleanField(default=False, verbose_name='deployment needed'),
        ),
        migrations.AlterField(
            model_name='surgealert',
            name='event',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.Event', verbose_name='event'),
        ),
        migrations.AlterField(
            model_name='surgealert',
            name='is_private',
            field=models.BooleanField(default=False, verbose_name='is private?'),
        ),
        migrations.AlterField(
            model_name='surgealert',
            name='message',
            field=models.TextField(verbose_name='message'),
        ),
        migrations.AlterField(
            model_name='surgealert',
            name='operation',
            field=models.CharField(max_length=100, verbose_name='operation'),
        ),
    ]
