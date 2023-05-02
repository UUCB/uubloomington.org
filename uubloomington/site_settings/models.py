from django.db import models

from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.fields import StreamField
from wagtail.blocks import RichTextBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.contrib.settings.models import BaseGenericSetting, register_setting


@register_setting
class SiteWideSettings(BaseGenericSetting):
    """Site-Wide Settings"""

    title = models.CharField(max_length=50, blank=True, null=True)
    subtitle = models.CharField(max_length=50, blank=True, null=True)
    tagline = models.CharField(max_length=200, blank=True, null=True)
    giving_url = models.CharField(max_length=200, blank=True, null=True)
    directions_url = models.CharField(max_length=2000, blank=True, null=True)
    header_announcement = models.CharField(max_length=50, blank=True, null=True )

    churchcenter_calendar_url = models.CharField(max_length=900, blank=True, null=True, help_text='Church Center Calendar URL')

    livestream_url = models.CharField(max_length=900, blank=True, null=True)

    panels = [
        MultiFieldPanel([
            FieldPanel('title'),
            FieldPanel('subtitle'),
            FieldPanel('tagline'),
            FieldPanel('giving_url'),
            FieldPanel('directions_url'),
            FieldPanel('header_announcement'),
        ], heading="Header Settings"),
        MultiFieldPanel([
            FieldPanel('churchcenter_calendar_url'),
        ], heading="Church Center Integration Settings"),
        MultiFieldPanel([
            FieldPanel('livestream_url'),
        ], heading="Livestream URL")
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
