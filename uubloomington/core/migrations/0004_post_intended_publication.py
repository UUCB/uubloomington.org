# Generated by Django 4.1.6 on 2023-04-25 19:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_post_publish_in_newsletter'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='intended_publication',
            field=models.DateField(default=datetime.date(1970, 1, 1)),
            preserve_default=False,
        ),
    ]
