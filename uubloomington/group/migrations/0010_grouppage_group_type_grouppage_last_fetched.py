# Generated by Django 4.2.1 on 2023-06-01 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0009_grouppage_featured_image_grouppage_summary_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='grouppage',
            name='group_type',
            field=models.BinaryField(null=True),
        ),
        migrations.AddField(
            model_name='grouppage',
            name='last_fetched',
            field=models.DateTimeField(null=True),
        ),
    ]
