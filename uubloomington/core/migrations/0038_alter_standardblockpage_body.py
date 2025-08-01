# Generated by Django 5.1 on 2024-11-27 17:10

import advanced_forms.models
import core.blocks
import wagtail.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0037_alter_standardblockpage_body"),
    ]

    operations = [
        migrations.AlterField(
            model_name="standardblockpage",
            name="body",
            field=wagtail.fields.StreamField(
                [
                    ("rich_text", 0),
                    ("read_more", 1),
                    ("show_featured_image", 2),
                    ("page_feature", 3),
                    ("expandable_list", 4),
                    ("embed", 5),
                    ("auto_index", 6),
                    ("selectable_index", 8),
                    ("document_list", 9),
                    ("badge_area", 14),
                    ("anchor", 15),
                    ("upcoming_service", 16),
                    ("upcoming_oos", 17),
                    ("multi_column", 19),
                    ("directions", 22),
                    ("page_tree_index", 8),
                    ("advanced_form", 23),
                    ("card_container", 25),
                    ("section", 32),
                    ("table_of_contents", 33),
                ],
                block_lookup={
                    0: ("wagtail.blocks.RichTextBlock", (), {}),
                    1: ("core.blocks.ReadMoreTagBlock", (), {}),
                    2: ("core.blocks.ShowFeaturedImageBlock", (), {}),
                    3: ("core.blocks.PageFeatureBlock", (), {}),
                    4: (
                        "wagtail.blocks.ListBlock",
                        (core.blocks.ExpandableListItemBlock,),
                        {},
                    ),
                    5: ("wagtail.embeds.blocks.EmbedBlock", (), {"max_height": 900}),
                    6: ("core.blocks.AutoIndexBlock", (), {}),
                    7: ("wagtail.blocks.PageChooserBlock", (), {}),
                    8: ("wagtail.blocks.StructBlock", [[("page", 7)]], {}),
                    9: ("core.blocks.DocumentListBlock", (), {}),
                    10: ("wagtail.images.blocks.ImageChooserBlock", (), {}),
                    11: ("wagtail.blocks.URLBlock", (), {}),
                    12: ("wagtail.blocks.CharBlock", (), {}),
                    13: (
                        "wagtail.blocks.StructBlock",
                        [[("image", 10), ("link", 11), ("link_text", 12)]],
                        {},
                    ),
                    14: ("core.blocks.BadgeAreaBlock", (13,), {}),
                    15: ("wagtail.blocks.StructBlock", [[("name", 12)]], {}),
                    16: ("core.blocks.UpcomingServiceBlock", (), {}),
                    17: ("core.blocks.UpcomingOrderOfServiceBlock", (), {}),
                    18: (
                        "wagtail.blocks.StreamBlock",
                        [[("rich_text", 0)]],
                        {"max_num": 3},
                    ),
                    19: ("wagtail.blocks.StreamBlock", [[("column", 18)]], {}),
                    20: (
                        "wagtail.images.blocks.ImageChooserBlock",
                        (),
                        {
                            "help_text": "Image associated with step in directions",
                            "required": False,
                        },
                    ),
                    21: (
                        "wagtail.blocks.StructBlock",
                        [[("title", 12), ("body", 0), ("image", 20)]],
                        {},
                    ),
                    22: ("wagtail.blocks.StreamBlock", [[("step", 21)]], {}),
                    23: (
                        "core.blocks.AdvancedFormBlock",
                        (advanced_forms.models.AdvancedForm,),
                        {},
                    ),
                    24: (
                        "wagtail.blocks.StructBlock",
                        [
                            [
                                ("title", 12),
                                ("body", 0),
                                ("image", 10),
                                ("action_text", 12),
                                ("action_link", 12),
                            ]
                        ],
                        {},
                    ),
                    25: ("wagtail.blocks.StreamBlock", [[("card", 24)]], {}),
                    26: ("core.blocks.BadgeAreaBlock", (), {"child_block": 13}),
                    27: (
                        "wagtail.blocks.StreamBlock",
                        [
                            [
                                ("rich_text", 0),
                                ("read_more", 1),
                                ("show_featured_image", 2),
                                ("page_feature", 3),
                                ("expandable_list", 4),
                                ("embed", 5),
                                ("auto_index", 6),
                                ("selectable_index", 8),
                                ("document_list", 9),
                                ("badge_area", 26),
                                ("anchor", 15),
                                ("upcoming_service", 16),
                                ("upcoming_oos", 17),
                                ("multi_column", 19),
                                ("directions", 22),
                                ("page_tree_index", 8),
                                ("advanced_form", 23),
                                ("card_container", 25),
                            ]
                        ],
                        {"required": False},
                    ),
                    28: (
                        "wagtail.blocks.StructBlock",
                        [[("heading", 12), ("body", 27)]],
                        {},
                    ),
                    29: (
                        "wagtail.blocks.StreamBlock",
                        [
                            [
                                ("rich_text", 0),
                                ("read_more", 1),
                                ("show_featured_image", 2),
                                ("page_feature", 3),
                                ("expandable_list", 4),
                                ("embed", 5),
                                ("auto_index", 6),
                                ("selectable_index", 8),
                                ("document_list", 9),
                                ("badge_area", 26),
                                ("anchor", 15),
                                ("upcoming_service", 16),
                                ("upcoming_oos", 17),
                                ("multi_column", 19),
                                ("directions", 22),
                                ("page_tree_index", 8),
                                ("advanced_form", 23),
                                ("card_container", 25),
                                ("sub_sub_section", 28),
                            ]
                        ],
                        {"required": False},
                    ),
                    30: (
                        "wagtail.blocks.StructBlock",
                        [[("heading", 12), ("body", 29)]],
                        {},
                    ),
                    31: (
                        "wagtail.blocks.StreamBlock",
                        [
                            [
                                ("rich_text", 0),
                                ("read_more", 1),
                                ("show_featured_image", 2),
                                ("page_feature", 3),
                                ("expandable_list", 4),
                                ("embed", 5),
                                ("auto_index", 6),
                                ("selectable_index", 8),
                                ("document_list", 9),
                                ("badge_area", 26),
                                ("anchor", 15),
                                ("upcoming_service", 16),
                                ("upcoming_oos", 17),
                                ("multi_column", 19),
                                ("directions", 22),
                                ("page_tree_index", 8),
                                ("advanced_form", 23),
                                ("card_container", 25),
                                ("sub_section", 30),
                            ]
                        ],
                        {"required": False},
                    ),
                    32: (
                        "wagtail.blocks.StructBlock",
                        [[("heading", 12), ("body", 31)]],
                        {},
                    ),
                    33: ("core.blocks.TableOfContentsBlock", (), {}),
                },
                null=True,
            ),
        ),
    ]
