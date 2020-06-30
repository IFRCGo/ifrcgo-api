# Generated by Django 2.2.13 on 2020-06-23 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0070_auto_20200618_0904'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='countrykeyfigure',
            options={'verbose_name': 'country key figure', 'verbose_name_plural': 'country key figures'},
        ),
        migrations.AlterModelOptions(
            name='regionkeyfigure',
            options={'verbose_name': 'region key figure', 'verbose_name_plural': 'region key figures'},
        ),
        migrations.AlterField(
            model_name='snippet',
            name='snippet',
            field=models.TextField(blank=True, null=True, verbose_name='snippet'),
        ),
    ]