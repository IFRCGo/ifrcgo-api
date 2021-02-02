# Generated by Django 2.2.13 on 2021-02-02 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0109_auto_20210201_0949'),
    ]

    operations = [
        migrations.AddField(
            model_name='fieldreport',
            name='notes_socioeco',
            field=models.TextField(blank=True, null=True, verbose_name='Description (Socioeconomic Interventions)'),
        ),
        migrations.AlterField(
            model_name='fieldreport',
            name='notes_health',
            field=models.TextField(blank=True, null=True, verbose_name='Description (Health)'),
        ),
        migrations.AlterField(
            model_name='fieldreport',
            name='notes_ns',
            field=models.TextField(blank=True, null=True, verbose_name='Description (NS Institutional Strengthening)'),
        ),
    ]