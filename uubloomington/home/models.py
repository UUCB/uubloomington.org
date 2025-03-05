import random

from django.db import models

from django.utils import timezone
from modelcluster.fields import ParentalKey
from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel

from core.blocks import BadgeAreaBlock, BadgeBlock, CardContainerBlock
from planningcenter_events.blocks import EventListingBlock
from planningcenter_events.models import EventListing
from services.models import OrderOfService


class HomePageCarouselImages(Orderable):
    page = ParentalKey("home.HomePage", related_name="carousel_images")
    carousel_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    header = models.TextField(max_length=25, null=True, blank=True)

    panels = [
        FieldPanel("carousel_image"),
        FieldPanel('header'),
    ]

    def prev_pk(self):
        return self.pk - 1


class HomePage(Page):
    parent_page_types = []
    services_home_page = models.OneToOneField(
        to='services.ServicesHomePage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    first_time_visitors_page = models.ForeignKey(
        to=Page,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    center_stage_header_text = models.CharField(max_length=100, null=True, blank=True)
    center_stage_body = RichTextField(null=True, blank=True)
    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [InlinePanel("carousel_images", min_num=1, label="Image")],
            heading="Carousel Images",
        ),
        MultiFieldPanel(
            [
                FieldPanel("center_stage_header_text"),
                FieldPanel("center_stage_body"),
            ],
            heading="Center Stage Section"
        ),
        FieldPanel("body"),
        FieldPanel("services_home_page"),
        FieldPanel("first_time_visitors_page"),
        FieldPanel("live_stream_page"),
    ]
    body = StreamField(
        block_types=[
            ('card_container', CardContainerBlock()),
            ('badge_area', BadgeAreaBlock(BadgeBlock())),
            ('event_listing', EventListingBlock(EventListing)),
        ],
        use_json_field=True,
        null=True,
    )
    live_stream_page = models.ForeignKey(
        to=Page,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        next_oos = (
            OrderOfService.objects.filter(date__gte=timezone.now())
            .order_by('date')
            .first()
        )
        if next_oos:
            context['next_service'] = next_oos.service.specific
        return context

    def get_carousel_image(self):
        return random.choice(self.carousel_images.all())
