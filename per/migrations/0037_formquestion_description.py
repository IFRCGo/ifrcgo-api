# Generated by Django 2.2.13 on 2020-11-30 14:16

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('per', '0036_auto_20201123_1055'),
    ]

    operations = [
        migrations.AddField(
            model_name='formquestion',
            name='description',
            field=tinymce.models.HTMLField(blank=True, null=True, verbose_name='description'),
        ),
    ]
