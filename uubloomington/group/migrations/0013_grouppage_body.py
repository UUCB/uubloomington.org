# Generated by Django 4.2.1 on 2023-06-03 02:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0012_grouppage_group_info'),
    ]

    operations = [
        migrations.AddField(
            model_name='grouppage',
            name='body',
            field=models.BooleanField(default=False),
        ),
    ]
