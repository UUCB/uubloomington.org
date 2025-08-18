from django.db import models
from wagtail.fields import StreamField
from wagtail.models import Page
from wagtail import blocks
from wagtail.admin.panels import FieldPanel, TabbedInterface, ObjectList

from kiosk.blocks import KioskContentBlock, KioskSidebarContentBlock


class KioskPage(Page):
    parent_page_types = ['home.HomePage']
    body = StreamField(
        [
            ("kiosk_content", KioskContentBlock()),
        ],
        collapsed=True,
    )
    sidebar = StreamField(
        [
            ("kiosk_sidebar", KioskSidebarContentBlock()),
        ],
        null=True,
        blank=True,
    )
    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]
    sidebar_panels = [
        FieldPanel("sidebar"),
    ]
    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading="Body"),
        ObjectList(sidebar_panels, heading="Sidebar"),
        ObjectList(Page.promote_panels, heading="Promote"),
    ])