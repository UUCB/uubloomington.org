# Generated by Django 4.1.6 on 2023-03-03 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_settings', '0003_sitewidesettings_churchcenter_calendar_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitewidesettings',
            name='livestream_url',
            field=models.CharField(blank=True, max_length=900, null=True),
        ),
    ]
