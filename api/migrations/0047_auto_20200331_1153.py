# Generated by Django 2.2.10 on 2020-03-31 11:53

import api.models
from django.db import migrations, models
import enumfields.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0046_merge_20200325_1016'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='tab_one_title',
            field=models.CharField(default='Additional Information', max_length=50),
        ),
        migrations.AddField(
            model_name='event',
            name='tab_three_title',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='tab_two_title',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='snippet',
            name='tab',
            field=enumfields.fields.EnumIntegerField(default=1, enum=api.models.TabNumber),
        ),
        migrations.AlterField(
            model_name='country',
            name='society_url',
            field=models.URLField(blank=True, verbose_name='URL - Society'),
        ),
        migrations.AlterField(
            model_name='country',
            name='url_ifrc',
            field=models.URLField(blank=True, verbose_name='URL - IFRC'),
        ),
    ]