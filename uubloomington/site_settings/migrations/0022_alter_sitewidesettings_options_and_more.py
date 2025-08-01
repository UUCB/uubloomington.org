# Generated by Django 5.1 on 2025-03-03 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("site_settings", "0021_sitewidesettings_max_fetched_planning_center_events"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="sitewidesettings",
            options={"verbose_name": "Site-Wide Settings"},
        ),
        migrations.AlterField(
            model_name="sitewidesettings",
            name="churchcenter_calendar_url",
            field=models.CharField(
                blank=True,
                help_text="URL of full Church Center calendar page",
                max_length=900,
                null=True,
                verbose_name="Church Center Calendar URL",
            ),
        ),
        migrations.AlterField(
            model_name="sitewidesettings",
            name="emergency_alert",
            field=models.CharField(
                blank=True,
                help_text="Shown in an eye-catching bright red box above the header. This should be used with caution to avoid it turning into wallpaper. Please add the date to your message if you choose to place it here.",
                max_length=5000,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="sitewidesettings",
            name="livestream_url",
            field=models.CharField(
                blank=True, max_length=900, null=True, verbose_name="Livestream URL"
            ),
        ),
        migrations.AlterField(
            model_name="sitewidesettings",
            name="shynet_ingress_url",
            field=models.CharField(
                blank=True,
                help_text="The first part of the shynet ingress URL - leave off the filename.",
                max_length=900,
                null=True,
                verbose_name="Shynet Ingress URL",
            ),
        ),
        migrations.AlterField(
            model_name="sitewidesettings",
            name="use_shynet",
            field=models.BooleanField(default=False, verbose_name="Use Shynet"),
        ),
    ]
