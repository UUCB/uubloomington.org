# Generated by Django 5.1 on 2025-05-28 19:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("services", "0035_alter_servicepage_body"),
    ]

    operations = [
        migrations.RenameField(
            model_name="servicepage",
            old_name="one_sentence",
            new_name="short_description",
        ),
    ]
