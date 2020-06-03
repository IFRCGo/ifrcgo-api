# Generated by Django 2.2.10 on 2020-06-03 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0066_merge_20200508_1241'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='action',
            options={'verbose_name': 'action', 'verbose_name_plural': 'actions'},
        ),
        migrations.AlterModelOptions(
            name='actionstaken',
            options={'verbose_name': 'actions taken', 'verbose_name_plural': 'all actions taken'},
        ),
        migrations.AlterModelOptions(
            name='admincontact',
            options={'verbose_name': 'admin contact', 'verbose_name_plural': 'admin contacts'},
        ),
        migrations.AlterModelOptions(
            name='adminkeyfigure',
            options={'ordering': ('source',), 'verbose_name': 'admin key figure', 'verbose_name_plural': 'admin key figures'},
        ),
        migrations.AlterModelOptions(
            name='adminlink',
            options={'verbose_name': 'admin link', 'verbose_name_plural': 'admin links'},
        ),
        migrations.AlterModelOptions(
            name='appeal',
            options={'ordering': ('-start_date', '-end_date'), 'verbose_name': 'appeal', 'verbose_name_plural': 'appeals'},
        ),
        migrations.AlterModelOptions(
            name='appealdocument',
            options={'verbose_name': 'appeal document', 'verbose_name_plural': 'appeal documents'},
        ),
        migrations.AlterModelOptions(
            name='authlog',
            options={'verbose_name': 'auth log', 'verbose_name_plural': 'auth logs'},
        ),
        migrations.AlterModelOptions(
            name='country',
            options={'ordering': ('name',), 'verbose_name': 'country', 'verbose_name_plural': 'countries'},
        ),
        migrations.AlterModelOptions(
            name='countrycontact',
            options={'verbose_name': 'country contact', 'verbose_name_plural': 'country contacts'},
        ),
        migrations.AlterModelOptions(
            name='countrykeyfigure',
            options={'ordering': ('source',), 'verbose_name': 'country key figure', 'verbose_name_plural': 'country key figures'},
        ),
        migrations.AlterModelOptions(
            name='countrylink',
            options={'verbose_name': 'country link', 'verbose_name_plural': 'country links'},
        ),
        migrations.AlterModelOptions(
            name='countrysnippet',
            options={'ordering': ('position', 'id'), 'verbose_name': 'country snippet', 'verbose_name_plural': 'country snippets'},
        ),
        migrations.AlterModelOptions(
            name='cronjob',
            options={'verbose_name': 'cronjob log record', 'verbose_name_plural': 'cronjob log records'},
        ),
        migrations.AlterModelOptions(
            name='disastertype',
            options={'ordering': ('name',), 'verbose_name': 'disaster type', 'verbose_name_plural': 'disaster types'},
        ),
        migrations.AlterModelOptions(
            name='district',
            options={'ordering': ('code',), 'verbose_name': 'district', 'verbose_name_plural': 'districts'},
        ),
        migrations.AlterModelOptions(
            name='emergencyoperationsdataset',
            options={'verbose_name': 'emergency operations dataset', 'verbose_name_plural': 'emergency operations datasets'},
        ),
        migrations.AlterModelOptions(
            name='emergencyoperationsea',
            options={'verbose_name': 'emergency operations emergency appeal', 'verbose_name_plural': 'emergency operations emergency appeals'},
        ),
        migrations.AlterModelOptions(
            name='emergencyoperationsfr',
            options={'verbose_name': 'emergency operations final report', 'verbose_name_plural': 'emergency operations final reports'},
        ),
        migrations.AlterModelOptions(
            name='emergencyoperationspeoplereached',
            options={'verbose_name': 'emergency operations people reached', 'verbose_name_plural': 'emergency operations people reached'},
        ),
        migrations.AlterModelOptions(
            name='event',
            options={'ordering': ('-disaster_start_date',), 'verbose_name': 'emergency', 'verbose_name_plural': 'emergencies'},
        ),
        migrations.AlterModelOptions(
            name='eventcontact',
            options={'verbose_name': 'event contact', 'verbose_name_plural': 'event contacts'},
        ),
        migrations.AlterModelOptions(
            name='fieldreport',
            options={'ordering': ('-created_at', '-updated_at'), 'verbose_name': 'field report', 'verbose_name_plural': 'field reports'},
        ),
        migrations.AlterModelOptions(
            name='fieldreportcontact',
            options={'verbose_name': 'field report contanct', 'verbose_name_plural': 'field report contancts'},
        ),
        migrations.AlterModelOptions(
            name='gdacsevent',
            options={'verbose_name': 'gdacs event', 'verbose_name_plural': 'gdacs events'},
        ),
        migrations.AlterModelOptions(
            name='keyfigure',
            options={'verbose_name': 'key figure', 'verbose_name_plural': 'key figures'},
        ),
        migrations.AlterModelOptions(
            name='profile',
            options={'verbose_name': 'user profile', 'verbose_name_plural': 'user profiles'},
        ),
        migrations.AlterModelOptions(
            name='region',
            options={'ordering': ('name',), 'verbose_name': 'region', 'verbose_name_plural': 'regions'},
        ),
        migrations.AlterModelOptions(
            name='regioncontact',
            options={'verbose_name': 'region contact', 'verbose_name_plural': 'region contacts'},
        ),
        migrations.AlterModelOptions(
            name='regionkeyfigure',
            options={'ordering': ('source',), 'verbose_name': 'region key figure', 'verbose_name_plural': 'region key figures'},
        ),
        migrations.AlterModelOptions(
            name='regionlink',
            options={'verbose_name': 'region link', 'verbose_name_plural': 'region links'},
        ),
        migrations.AlterModelOptions(
            name='regionsnippet',
            options={'ordering': ('position', 'id'), 'verbose_name': 'region snippet', 'verbose_name_plural': 'region snippets'},
        ),
        migrations.AlterModelOptions(
            name='reversiondifferencelog',
            options={'verbose_name': 'reversion difference log', 'verbose_name_plural': 'reversion difference logs'},
        ),
        migrations.AlterModelOptions(
            name='situationreport',
            options={'verbose_name': 'situation report', 'verbose_name_plural': 'situation reports'},
        ),
        migrations.AlterModelOptions(
            name='situationreporttype',
            options={'verbose_name': 'situation report type', 'verbose_name_plural': 'situation report types'},
        ),
        migrations.AlterModelOptions(
            name='snippet',
            options={'ordering': ('position', 'id'), 'verbose_name': 'snippet', 'verbose_name_plural': 'snippets'},
        ),
        migrations.AlterModelOptions(
            name='source',
            options={'verbose_name': 'source', 'verbose_name_plural': 'sources'},
        ),
        migrations.AlterModelOptions(
            name='sourcetype',
            options={'verbose_name': 'source type', 'verbose_name_plural': 'source types'},
        ),
        migrations.AlterField(
            model_name='actionstaken',
            name='actions',
            field=models.ManyToManyField(blank=True, to='api.Action'),
        ),
    ]
