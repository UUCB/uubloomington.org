from django.db import models

from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import StreamField
from wagtail.blocks import RichTextBlock, StructBlock, CharBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.contrib.settings.models import BaseGenericSetting, register_setting
from wagtail.models import Page


@register_setting
class SiteWideSettings(BaseGenericSetting):
    """Site-Wide Settings"""

    title = models.CharField(max_length=50, blank=True, null=True)
    subtitle = models.CharField(max_length=50, blank=True, null=True)
    tagline = models.CharField(max_length=200, blank=True, null=True)
    header_announcement = models.CharField(max_length=50, blank=True, null=True )
    header_links = StreamField(
        [
            (
                'url', StructBlock(
                    [
                        ('text', CharBlock()),
                        ('destination', CharBlock()),
                    ],
                    icon='globe',
                )
            )
        ],
        use_json_field=True,
        null=True,
    )

    churchcenter_calendar_url = models.CharField(max_length=900, blank=True, null=True, help_text='Church Center Calendar URL')

    livestream_url = models.CharField(max_length=900, blank=True, null=True)

    internal_livestream_page = models.ForeignKey(
        to=Page,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+',
    )

    refresh_from_planningcenter_every = models.IntegerField(default=5)

    panels = [
        MultiFieldPanel([
            FieldPanel('title'),
            FieldPanel('subtitle'),
            FieldPanel('tagline'),
            FieldPanel('header_announcement'),
        ], heading="Header Settings"),
        MultiFieldPanel([
            FieldPanel('churchcenter_calendar_url'),
        ], heading="Church Center Integration Settings"),
        MultiFieldPanel([
            FieldPanel('livestream_url'),
            FieldPanel('internal_livestream_page'),
        ], heading="Livestream URL"),
        FieldPanel('header_links'),
        MultiFieldPanel([
            FieldPanel('refresh_from_planningcenter_every'),
        ], heading="Planning Center Integration Settings")
    ]


@register_setting
class FooterSettings(BaseGenericSetting):
    """Footer Content Settings"""
    minister_feature_heading = models.CharField(max_length=50)
    minister_feature = models.OneToOneField(
        to='core.PageWithPosts',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    additional_content = StreamField(
        [
            ('text', RichTextBlock()),
            ('image', ImageChooserBlock()),
        ],
        max_num=3,
        use_json_field=True,
        null=True,
    )

    panels = [
        MultiFieldPanel([
            FieldPanel('minister_feature_heading'),
            FieldPanel('minister_feature'),
        ], heading='Minister Feature'),
        FieldPanel("additional_content"),
    ]
