# Generated by Django 2.0.12 on 2019-10-07 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0024_eventcontact_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='fieldreportcontact',
            name='phone',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
