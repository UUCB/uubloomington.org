# Generated by Django 4.2.1 on 2023-05-22 22:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_listpage_listpageitem'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listpageitem',
            name='body',
        ),
    ]
