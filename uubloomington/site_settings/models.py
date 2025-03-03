from django.db import models

from wagtail.admin.panels import FieldPanel, TabbedInterface, ObjectList
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

    footer_content = StreamField(
        [
            ('footer_text', RichTextBlock()),
        ],
        use_json_field=True,
        null=True,
        blank=True,
        help_text='Each of these blocks should ideally be quite short single lines. These are displayed in a row across the site footer.',
        verbose_name='Footer Content',
    )

    copyright_notice = models.CharField(
        max_length=70,
        blank=True,
        null=True,
        help_text='Displayed below footer content.',
        verbose_name='Copyright Notice',
    )

    churchcenter_calendar_url = models.CharField(
        max_length=900,
        blank=True,
        null=True,
        help_text='URL of full Church Center calendar page',
        verbose_name='Church Center Calendar URL',
    )

    max_fetched_planning_center_events = models.PositiveSmallIntegerField(
        default=200,
        blank=False,
        null=False,
        help_text='Maximum number of calendar events to fetch from Planning Center at a time',
    )

    livestream_url = models.CharField(
        max_length=900,
        blank=True,
        null=True,
        verbose_name="Livestream URL",
    )

    emergency_alert = models.CharField(
        max_length=5000,
        blank=True,
        null=True,
        help_text='Shown in an eye-catching bright red box above the header. This should be used with caution to avoid it turning into wallpaper. Please add the date to your message if you choose to place it here.',
    )

    internal_livestream_page = models.ForeignKey(
        to=Page,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+',
    )

    refresh_from_planningcenter_every = models.IntegerField(default=5)

    use_shynet = models.BooleanField(
        default=False,
        verbose_name='Use Shynet',
    )
    shynet_ingress_url = models.CharField(
        max_length=900,
        blank=True,
        null=True,
        help_text='The first part of the shynet ingress URL - leave off the filename.',
        verbose_name='Shynet Ingress URL',
    )

    header_panels = [
        FieldPanel('title'),
        FieldPanel('subtitle'),
        FieldPanel('tagline'),
        FieldPanel('header_announcement'),
        FieldPanel('emergency_alert'),
        FieldPanel('header_links'),
    ]

    planningcenter_panels = [
        FieldPanel('refresh_from_planningcenter_every'),
        FieldPanel('max_fetched_planning_center_events'),
        FieldPanel('churchcenter_calendar_url'),
    ]

    analytics_panels = [
        FieldPanel('use_shynet'),
        FieldPanel('shynet_ingress_url'),
    ]

    livestream_panels = [
        FieldPanel('livestream_url'),
        FieldPanel('internal_livestream_page'),
    ]

    footer_panels = [
        FieldPanel('footer_content'),
        FieldPanel('copyright_notice'),
    ]

    edit_handler = TabbedInterface([
        ObjectList(header_panels, heading='Header'),
        ObjectList(footer_panels, heading='Footer'),
        ObjectList(planningcenter_panels, heading='Planning Center/Church Center Integration'),
        ObjectList(analytics_panels, heading='Analytics'),
        ObjectList(livestream_panels, heading='Livestream'),
    ])

    class Meta:
        verbose_name = 'Site-Wide Settings'
