# Generated by Django 5.1 on 2025-03-03 20:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("site_settings", "0023_sitewidesettings_copyright_notice_and_more"),
    ]

    operations = [
        migrations.DeleteModel(
            name="FooterSettings",
        ),
    ]
