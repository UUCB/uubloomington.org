from django.db import models

from modelcluster.fields import ParentalKey
from wagtail.models import Page, Orderable, Site
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.contrib import settings
from site_settings.models import SiteWideSettings


def get_default_stream_url():
    return SiteWideSettings.load().livestream_url


class ServicesHomePage(Page):
    body = RichTextField(blank=True, null=True)


class ServicePage(Page):
    body = RichTextField(blank=True, null=True)
    vimeo_link = models.CharField(max_length=100, blank=False, null=True, default=get_default_stream_url)
    order_of_service_link = models.CharField(max_length=900, blank=True, null=True)

    parent_page_types = ['ServicesHomePage']

    content_panels = Page.content_panels + [
        FieldPanel('body'),
        MultiFieldPanel(
            [InlinePanel('participants', label="Participant")],
            heading="Participants"
        ),
        FieldPanel('vimeo_link'),
        FieldPanel('order_of_service_link'),
    ]


class Participant(Orderable):
    # copy_from = models.ForeignKey(unique=False)
    service = ParentalKey("services.ServicePage", related_name='participants')
    name = models.CharField(max_length=100, blank=True, null=False)
    bio = RichTextField(blank=True, null=True)

    panels = [
        FieldPanel('name'),
        FieldPanel('bio'),
    ]


# Create your models here.
