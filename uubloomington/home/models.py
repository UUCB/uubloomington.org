import random

from django.db import models

from django.utils import timezone
from modelcluster.fields import ParentalKey
from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel, TabbedInterface, ObjectList

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
    is_homepage = True
    parent_page_types = []
    services_home_page = models.OneToOneField(
        to='services.ServicesHomePage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Services home page',
        help_text='Page to link to the "All Services" button below the upcoming service.'
    )
    first_time_visitors_page = models.ForeignKey(
        to=Page,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='"First Time Visitors" page',
        help_text='Page to link to the "First Time Visitor?" button below the upcoming service'
    )
    center_stage_header_text = models.CharField(max_length=100, null=True, blank=True)
    center_stage_body = RichTextField(null=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]

    carousel_panels = [
        MultiFieldPanel(
            [InlinePanel("carousel_images", min_num=1, label="Image")],
            heading="Carousel Images",
        ),
    ]

    center_stage_panels = [
        FieldPanel("center_stage_header_text"),
        FieldPanel("center_stage_body"),
    ]

    settings_panels = [
        FieldPanel("services_home_page"),
        FieldPanel("first_time_visitors_page"),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading="Body"),
        ObjectList(carousel_panels, heading="Carousel Images"),
        ObjectList(center_stage_panels, heading="Center Stage"),
        ObjectList(settings_panels, heading="Settings"),
        ObjectList(Page.promote_panels, heading="Promote"),
    ])

    body = StreamField(
        block_types=[
            ('card_container', CardContainerBlock()),
            ('badge_area', BadgeAreaBlock(BadgeBlock())),
            ('event_listing', EventListingBlock(EventListing)),
        ],
        use_json_field=True,
        null=True,
    )

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        next_services = [
            oos.service.specific
            for oos
            in OrderOfService.objects.filter(date__gte=timezone.now()).order_by('date')[:2]
        ]
        context['next_services'] = next_services
        return context

    def get_carousel_image(self):
        return random.choice(self.carousel_images.all())
