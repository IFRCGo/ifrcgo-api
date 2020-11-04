# Generated by Django 2.2.13 on 2020-11-04 03:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deployments', '0032_auto_20200729_0934'),
    ]

    operations = [
        migrations.CreateModel(
            name='MolnixTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('molnix_id', models.IntegerField()),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=512)),
                ('color', models.CharField(max_length=6)),
                ('tag_type', models.CharField(max_length=127)),
            ],
        ),
    ]
