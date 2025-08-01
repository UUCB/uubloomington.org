# Generated by Django 4.2.1 on 2023-05-15 22:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0025_alter_image_file_alter_rendition_file'),
        ('services', '0011_alter_orderofservice_program_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicepage',
            name='featured_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='wagtailimages.image'),
        ),
    ]
