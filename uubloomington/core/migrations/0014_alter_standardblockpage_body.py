# Generated by Django 4.2.1 on 2023-06-03 20:49

import core.blocks
from django.db import migrations
import wagtail.blocks
import wagtail.embeds.blocks
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_alter_standardblockpage_body'),
    ]

    operations = [
        migrations.AlterField(
            model_name='standardblockpage',
            name='body',
            field=wagtail.fields.StreamField([('rich_text', wagtail.blocks.RichTextBlock()), ('read_more', core.blocks.ReadMoreTagBlock()), ('show_featured_image', core.blocks.ShowFeaturedImageBlock()), ('page_feature', core.blocks.PageFeatureBlock()), ('expandable_list', wagtail.blocks.ListBlock(core.blocks.ExpandableListItemBlock)), ('embed', wagtail.embeds.blocks.EmbedBlock(max_height=900)), ('auto_index', core.blocks.AutoIndexBlock())], null=True, use_json_field=True),
        ),
    ]
