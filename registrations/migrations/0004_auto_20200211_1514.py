# Generated by Django 2.2.9 on 2020-02-11 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registrations', '0003_auto_20200206_0926'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pending',
            name='admin_1_validated_date',
            field=models.DateTimeField(blank=True, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='pending',
            name='admin_2_validated_date',
            field=models.DateTimeField(blank=True, editable=False, null=True),
        ),
    ]