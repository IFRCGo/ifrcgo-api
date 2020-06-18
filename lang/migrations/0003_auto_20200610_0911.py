# Generated by Django 2.2.10 on 2020-06-10 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lang', '0002_auto_20200603_0613'),
    ]

    operations = [
        migrations.AddField(
            model_name='string',
            name='hash',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='language',
            name='code',
            field=models.CharField(choices=[('en', 'English'), ('es', 'Spanish'), ('fr', 'French'), ('ar', 'Arabic')], max_length=255, unique=True),
        ),
    ]