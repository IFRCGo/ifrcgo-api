# Generated by Django 2.2.13 on 2020-09-16 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0088_auto_20200916_0834'),
    ]

    operations = [
        migrations.AlterField(
            model_name='situationreporttype',
            name='type',
            field=models.CharField(max_length=150, verbose_name='type'),
        ),
        migrations.AlterField(
            model_name='situationreporttype',
            name='type_ar',
            field=models.CharField(max_length=150, null=True, verbose_name='type'),
        ),
        migrations.AlterField(
            model_name='situationreporttype',
            name='type_en',
            field=models.CharField(max_length=150, null=True, verbose_name='type'),
        ),
        migrations.AlterField(
            model_name='situationreporttype',
            name='type_es',
            field=models.CharField(max_length=150, null=True, verbose_name='type'),
        ),
        migrations.AlterField(
            model_name='situationreporttype',
            name='type_fr',
            field=models.CharField(max_length=150, null=True, verbose_name='type'),
        ),
    ]
