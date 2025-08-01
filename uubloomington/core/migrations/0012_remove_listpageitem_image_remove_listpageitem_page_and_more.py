# Generated by Django 4.2.1 on 2023-05-24 20:35

import core.blocks
from django.db import migrations
import wagtail.blocks
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_standardblockpage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listpageitem',
            name='image',
        ),
        migrations.RemoveField(
            model_name='listpageitem',
            name='page',
        ),
        migrations.AlterField(
            model_name='standardblockpage',
            name='body',
            field=wagtail.fields.StreamField([('rich_text', wagtail.blocks.RichTextBlock()), ('read_more', core.blocks.ReadMoreTagBlock()), ('show_featured_image', core.blocks.ShowFeaturedImageBlock()), ('page_feature', core.blocks.PageFeatureBlock()), ('expandable_list', wagtail.blocks.ListBlock(core.blocks.ExpandableListItemBlock))], null=True, use_json_field=True),
        ),
        migrations.DeleteModel(
            name='ListPage',
        ),
        migrations.DeleteModel(
            name='ListPageItem',
        ),
    ]
