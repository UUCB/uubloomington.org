# Generated by Django 5.0.2 on 2024-03-13 18:08

import services.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0020_servicepage_show_video_embed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicepage',
            name='vimeo_link',
            field=models.CharField(blank=True, default=services.models.get_default_stream_url, max_length=100, null=True),
        ),
    ]
