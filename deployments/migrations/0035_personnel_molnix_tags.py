# Generated by Django 2.2.13 on 2020-11-11 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deployments', '0034_auto_20201111_1056'),
    ]

    operations = [
        migrations.AddField(
            model_name='personnel',
            name='molnix_tags',
            field=models.ManyToManyField(blank=True, to='deployments.MolnixTag'),
        ),
    ]
