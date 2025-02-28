import random
import pickle

from django.db import models

from django.utils import timezone
from modelcluster.fields import ParentalKey
from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel

from services.models import OrderOfService

from core.planningcenter_extras import Event  # Needed to un-pickle upcoming events


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


class HomePageCard(Orderable):
    page = ParentalKey("home.HomePage", related_name="cards")
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    title = models.CharField(max_length=30)
    body = RichTextField(max_length=400)
    action_url = models.CharField(max_length=1000)
    action_text = models.CharField(max_length=30)

    panels = [
        FieldPanel('image'),
        FieldPanel('title'),
        FieldPanel('body'),
        MultiFieldPanel([
            FieldPanel('action_text'),
            FieldPanel('action_url'),
        ],
        heading="Action"
        )
    ]


class HomePageBadge(Orderable):
    page = ParentalKey("home.HomePage", related_name="badges")
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    text = RichTextField(max_length=100, null=True)
    url = models.URLField()
    panels = [
        FieldPanel('image'),
        FieldPanel('url'),
        FieldPanel('text', heading='Text to be displayed under the badge'),
    ]


class HomePage(Page):
    parent_page_types = []
    display_next_events = models.IntegerField(default=10)
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
        MultiFieldPanel(
            [InlinePanel("cards", max_num=6, min_num=2, label="Card")],
            heading="Cards"
        ),
        MultiFieldPanel(
            [InlinePanel("badges", max_num=6, label="Badge")],
            heading="Badges"
        ),
        FieldPanel("services_home_page"),
        FieldPanel("first_time_visitors_page"),
        FieldPanel("display_next_events"),
        FieldPanel("live_stream_page"),
        FieldPanel("show_upcoming_events"),
    ]

    upcoming_events_last_checked = models.DateTimeField(default=timezone.make_aware(timezone.datetime.min))
    upcoming_events = models.BinaryField(null=True)  # Pickled Events
    show_upcoming_events = models.BooleanField(default=True, null=False, help_text='Show "Upcoming Events" card using legacy hacks')
    live_stream_page = models.ForeignKey(
        to=Page,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['upcoming_events'] = pickle.loads(self.upcoming_events)
        next_oos = (
            OrderOfService.objects.filter(date__gte=timezone.now())
            .order_by('date')
            .first()
        )
        if next_oos:
            context['next_service'] = next_oos.service.specific
        if len(self.cards.all()) == 4:
            context['has_4'] = 'has_4'
        return context

    def get_carousel_image(self):
        return random.choice(self.carousel_images.all())
