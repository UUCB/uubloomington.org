# Generated by Django 4.2.1 on 2023-06-03 02:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0014_remove_grouppage_body'),
    ]

    operations = [
        migrations.AddField(
            model_name='grouppage',
            name='body',
            field=models.BooleanField(default=False),
        ),
    ]
