from django.db import models
from wagtail.fields import StreamField
from wagtail.models import Page
from wagtail import blocks
from wagtail.admin.panels import FieldPanel

from kiosk.blocks import KioskContentBlock


class KioskPage(Page):
    parent_page_types = ['home.HomePage']
    body = StreamField(
        [
            ("kiosk_content", KioskContentBlock()),
        ]
    )
    sidebar = StreamField(
        [
            ("rich_text", blocks.RichTextBlock()),
        ]
    )
    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]