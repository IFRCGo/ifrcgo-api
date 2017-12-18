# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2017-12-18 15:17
from __future__ import unicode_literals

import api.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import enumfields.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ActionsTaken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('organization', models.CharField(choices=[('NTLS', 'National Society'), ('PNS', 'Foreign Society'), ('FDRN', 'Federation')], max_length=4)),
                ('summary', models.TextField(blank=True)),
                ('actions', models.ManyToManyField(to='api.Action')),
            ],
        ),
        migrations.CreateModel(
            name='Appeal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aid', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=100)),
                ('atype', enumfields.fields.EnumIntegerField(default=0, enum=api.models.AppealType)),
                ('status', models.CharField(blank=True, max_length=30)),
                ('code', models.CharField(max_length=20, null=True)),
                ('sector', models.CharField(blank=True, max_length=100)),
                ('num_beneficiaries', models.IntegerField(default=0)),
                ('amount_requested', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('amount_funded', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('start_date', models.DateTimeField(null=True)),
                ('end_date', models.DateTimeField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ('-end_date', '-start_date'),
            },
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ctype', models.CharField(blank=True, max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=300)),
                ('email', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('iso', models.CharField(max_length=2, null=True)),
                ('society_name', models.TextField(blank=True)),
                ('society_url', models.URLField(blank=True)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='DisasterType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('summary', models.TextField()),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='ERU',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', enumfields.fields.EnumIntegerField(default=0, enum=api.models.ERUType)),
                ('units', models.IntegerField(default=0)),
                ('countries', models.ManyToManyField(blank=True, to='api.Country')),
            ],
        ),
        migrations.CreateModel(
            name='ERUOwner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('country', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.Country')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('summary', models.TextField(blank=True)),
                ('embed_snippet', models.CharField(blank=True, max_length=300, null=True)),
                ('num_affected', models.IntegerField(blank=True, null=True)),
                ('disaster_start_date', models.DateTimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('auto_generated', models.BooleanField(default=False)),
                ('contacts', models.ManyToManyField(to='api.Contact')),
                ('countries', models.ManyToManyField(to='api.Country')),
                ('dtype', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.DisasterType')),
            ],
            options={
                'ordering': ('-disaster_start_date',),
            },
        ),
        migrations.CreateModel(
            name='FieldReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rid', models.CharField(max_length=100)),
                ('summary', models.TextField(blank=True)),
                ('description', models.TextField(blank=True, default='')),
                ('status', models.IntegerField(default=0)),
                ('request_assistance', models.BooleanField(default=False)),
                ('num_injured', models.IntegerField(blank=True, null=True)),
                ('num_dead', models.IntegerField(blank=True, null=True)),
                ('num_missing', models.IntegerField(blank=True, null=True)),
                ('num_affected', models.IntegerField(blank=True, null=True)),
                ('num_displaced', models.IntegerField(blank=True, null=True)),
                ('num_assisted', models.IntegerField(blank=True, null=True)),
                ('num_localstaff', models.IntegerField(blank=True, null=True)),
                ('num_volunteers', models.IntegerField(blank=True, null=True)),
                ('num_expats_delegates', models.IntegerField(blank=True, null=True)),
                ('gov_num_injured', models.IntegerField(blank=True, null=True)),
                ('gov_num_dead', models.IntegerField(blank=True, null=True)),
                ('gov_num_missing', models.IntegerField(blank=True, null=True)),
                ('gov_num_affected', models.IntegerField(blank=True, null=True)),
                ('gov_num_displaced', models.IntegerField(blank=True, null=True)),
                ('gov_num_assisted', models.IntegerField(blank=True, null=True)),
                ('actions_others', models.TextField(blank=True, null=True)),
                ('visibility', enumfields.fields.EnumIntegerField(default=1, enum=api.models.VisibilityChoices)),
                ('bulletin', enumfields.fields.EnumIntegerField(default=0, enum=api.models.RequestChoices)),
                ('dref', enumfields.fields.EnumIntegerField(default=0, enum=api.models.RequestChoices)),
                ('dref_amount', models.IntegerField(blank=True, null=True)),
                ('appeal', enumfields.fields.EnumIntegerField(default=0, enum=api.models.RequestChoices)),
                ('appeal_amount', models.IntegerField(blank=True, null=True)),
                ('rdrt', enumfields.fields.EnumIntegerField(default=0, enum=api.models.RequestChoices)),
                ('num_rdrt', models.IntegerField(blank=True, null=True)),
                ('fact', enumfields.fields.EnumIntegerField(default=0, enum=api.models.RequestChoices)),
                ('num_fact', models.IntegerField(blank=True, null=True)),
                ('ifrc_staff', enumfields.fields.EnumIntegerField(default=0, enum=api.models.RequestChoices)),
                ('num_ifrc_staff', models.IntegerField(blank=True, null=True)),
                ('eru_base_camp', enumfields.fields.EnumIntegerField(default=0, enum=api.models.RequestChoices)),
                ('eru_base_camp_units', models.IntegerField(blank=True, null=True)),
                ('eru_basic_health_care', enumfields.fields.EnumIntegerField(default=0, enum=api.models.RequestChoices)),
                ('eru_basic_health_care_units', models.IntegerField(blank=True, null=True)),
                ('eru_it_telecom', enumfields.fields.EnumIntegerField(default=0, enum=api.models.RequestChoices)),
                ('eru_it_telecom_units', models.IntegerField(blank=True, null=True)),
                ('eru_logistics', enumfields.fields.EnumIntegerField(default=0, enum=api.models.RequestChoices)),
                ('eru_logistics_units', models.IntegerField(blank=True, null=True)),
                ('eru_deployment_hospital', enumfields.fields.EnumIntegerField(default=0, enum=api.models.RequestChoices)),
                ('eru_deployment_hospital_units', models.IntegerField(blank=True, null=True)),
                ('eru_referral_hospital', enumfields.fields.EnumIntegerField(default=0, enum=api.models.RequestChoices)),
                ('eru_referral_hospital_units', models.IntegerField(blank=True, null=True)),
                ('eru_relief', enumfields.fields.EnumIntegerField(default=0, enum=api.models.RequestChoices)),
                ('eru_relief_units', models.IntegerField(blank=True, null=True)),
                ('eru_water_sanitation_15', enumfields.fields.EnumIntegerField(default=0, enum=api.models.RequestChoices)),
                ('eru_water_sanitation_15_units', models.IntegerField(blank=True, null=True)),
                ('eru_water_sanitation_40', enumfields.fields.EnumIntegerField(default=0, enum=api.models.RequestChoices)),
                ('eru_water_sanitation_40_units', models.IntegerField(blank=True, null=True)),
                ('eru_water_sanitation_20', enumfields.fields.EnumIntegerField(default=0, enum=api.models.RequestChoices)),
                ('eru_water_sanitation_20_units', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('contacts', models.ManyToManyField(to='api.Contact')),
                ('countries', models.ManyToManyField(to='api.Country')),
                ('dtype', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='api.DisasterType')),
                ('event', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='field_reports', to='api.Event')),
            ],
            options={
                'ordering': ('-created_at', '-updated_at'),
            },
        ),
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
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='profile', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('org', models.CharField(blank=True, max_length=100)),
                ('org_type', models.CharField(blank=True, choices=[('NTLS', 'National Society'), ('DLGN', 'Delegation'), ('SCRT', 'Secretariat'), ('ICRC', 'ICRC')], max_length=4)),
                ('city', models.CharField(blank=True, max_length=100)),
                ('department', models.CharField(blank=True, max_length=100)),
                ('position', models.CharField(blank=True, max_length=100)),
                ('phone_number', models.CharField(blank=True, max_length=100)),
                ('country', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.Country')),
            ],
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', enumfields.fields.EnumIntegerField(enum=api.models.RegionName)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('spec', models.TextField(blank=True)),
                ('field_report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.FieldReport')),
            ],
        ),
        migrations.CreateModel(
            name='SourceType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
            ],
        ),
        migrations.AddField(
            model_name='source',
            name='stype',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='api.SourceType'),
        ),
        migrations.AddField(
            model_name='fieldreport',
            name='regions',
            field=models.ManyToManyField(to='api.Region'),
        ),
        migrations.AddField(
            model_name='fieldreport',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='event',
            name='regions',
            field=models.ManyToManyField(to='api.Region'),
        ),
        migrations.AddField(
            model_name='eru',
            name='eru_owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.ERUOwner'),
        ),
        migrations.AddField(
            model_name='country',
            name='region',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.Region'),
        ),
        migrations.AddField(
            model_name='appeal',
            name='country',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.Country'),
        ),
        migrations.AddField(
            model_name='appeal',
            name='dtype',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.DisasterType'),
        ),
        migrations.AddField(
            model_name='appeal',
            name='event',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='appeals', to='api.Event'),
        ),
        migrations.AddField(
            model_name='appeal',
            name='region',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.Region'),
        ),
        migrations.AddField(
            model_name='actionstaken',
            name='field_report',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.FieldReport'),
        ),
    ]
