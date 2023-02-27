from django.db import models

from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.contrib.settings.models import BaseSetting, register_setting


@register_setting
class SiteWideSettings(BaseSetting):
    """Site-Wide Settings"""

    title = models.CharField(max_length=50, blank=True, null=True)
    subtitle = models.CharField(max_length=50, blank=True, null=True)
    tagline = models.CharField(max_length=200, blank=True, null=True)

    panels = [
        MultiFieldPanel([
            FieldPanel('title'),
            FieldPanel('subtitle'),
            FieldPanel('tagline'),
        ], heading="Header Settings")
    ]