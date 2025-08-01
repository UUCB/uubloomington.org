# Generated by Django 5.1.4 on 2025-02-11 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('planning_center_instance_id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('planning_center_event_id', models.IntegerField()),
                ('just_imported', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=255)),
                ('link', models.URLField(max_length=255)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('description', models.TextField()),
            ],
        ),
    ]
