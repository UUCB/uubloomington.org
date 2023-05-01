import datetime

import pypco
from django.db import models

from django.conf import settings
from modelcluster.fields import ParentalKey
from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField
from django.db.models import CharField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel


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
    title = models.CharField(max_length=20)
    body = RichTextField(max_length=400)
    action_url = models.CharField(max_length=1000)
    action_text = models.CharField(max_length=20)

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


class HomePage(Page):
    body = RichTextField(blank=True)
    # upcoming_events_offset = django_models.IntegerField(editable=False, null=True, blank=True)
    parent_page_types = []
    content_panels = Page.content_panels + [
        FieldPanel('body'),
        MultiFieldPanel(
            [InlinePanel("carousel_images", max_num=5, min_num=1, label="Image")],
            heading="Carousel Images",
        ),
        MultiFieldPanel(
            [InlinePanel("cards", max_num=6, min_num=2, label="Card")],
            heading="Cards"
        )
    ]

    def upcoming_events(self):  # Generate some placeholder events for now. Eventually, this will somehow pull from PC
        return [
            Event(
                name='Website Design Meeting',
                link='https://example.com',
                start_time=datetime.datetime(
                    year=2023,
                    month=2,
                    day=14,
                    hour=8,
                    minute=00,
                ),
                end_time=datetime.datetime(
                    year=2023,
                    month=2,
                    day=14,
                    hour=9,
                    minute=00,
                )
            ),
            Event(
                name='Staff Lunch',
                link='https://example.com',
                start_time=datetime.datetime(
                    year=2023,
                    month=2,
                    day=16,
                    hour=11,
                    minute=00,
                ),
                end_time=datetime.datetime(
                    year=2023,
                    month=2,
                    day=16,
                    hour=12,
                    minute=00,
                )
            ),
            Event(
                name='Order of Service Meeting',
                link='https://example.com',
                start_time=datetime.datetime(
                    year=2023,
                    month=2,
                    day=16,
                    hour=13,
                    minute=00,
                ),
                end_time=datetime.datetime(
                    year=2023,
                    month=2,
                    day=16,
                    hour=13,
                    minute=15,
                )
            ),
            Event(
                name='Core Staff Meeting',
                link='https://example.com',
                start_time=datetime.datetime(
                    year=2023,
                    month=2,
                    day=16,
                    hour=13,
                    minute=30,
                ),
                end_time=datetime.datetime(
                    year=2023,
                    month=2,
                    day=16,
                    hour=14,
                    minute=30,
                )
            ),
            Event(
                name='Choir Rehearsal',
                link='https://example.com',
                start_time=datetime.datetime(
                    year=2023,
                    month=2,
                    day=16,
                    hour=19,
                    minute=00,
                ),
                end_time=datetime.datetime(
                    year=2023,
                    month=2,
                    day=14,
                    hour=20,
                    minute=30,
                )
            )
        ]


class Event():  # Eventually, this should be replaced with an external module
    def __init__(self, name:str, link:str, start_time:datetime.datetime, end_time:datetime.datetime):
        self.name = name
        self.link = link
        self.start_time = start_time
        self.end_time = end_time

    def readable_times(self):
        return {
            'date': self.start_time.strftime('%A, %b. %d'),
            'start_time': self.start_time.strftime('%I:%M %p'),
            'end_time': self.end_time.strftime('%I:%M %p'),
        }