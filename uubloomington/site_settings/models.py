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

    emergency_alert = models.CharField(max_length=5000, blank=True, null=True)

    internal_livestream_page = models.ForeignKey(
        to=Page,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+',
    )

    refresh_from_planningcenter_every = models.IntegerField(default=5)

    use_shynet = models.BooleanField(default=False)
    shynet_ingress_url = models.CharField(max_length=900, blank=True, null=True, help_text='The first part of the shynet ingress URL - leave off the filename.')

    panels = [
        MultiFieldPanel([
            FieldPanel('title'),
            FieldPanel('subtitle'),
            FieldPanel('tagline'),
            FieldPanel('header_announcement'),
            FieldPanel('emergency_alert'),
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
        ], heading="Planning Center Integration Settings"),
        MultiFieldPanel(
            children=[
                FieldPanel('use_shynet'),
                FieldPanel('shynet_ingress_url'),
            ],
            heading="Shynet Integration Settings",
        )
    ]


@register_setting
class FooterSettings(BaseGenericSetting):
    """Footer Content Settings"""
    copyright_notice = models.CharField(
        max_length=70,
        blank=True,
        null=True,
        help_text='Copyright Notice - displayed in footer'
    )
    content = StreamField(
        [
            ('footer_text', RichTextBlock()),
        ],
        use_json_field=True,
        null=True,
        blank=True,
    )