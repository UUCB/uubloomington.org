import datetime
import random
import pickle
import zoneinfo

import pypco
from django.db import models

from site_settings.models import SiteWideSettings

from django.utils import timezone
from django.utils.dateparse import parse_datetime

from django.conf import settings

from modelcluster.fields import ParentalKey
from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel

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
    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [InlinePanel("carousel_images", max_num=5, min_num=1, label="Image")],
            heading="Carousel Images",
        ),
        MultiFieldPanel(
            [InlinePanel("cards", max_num=6, min_num=2, label="Card")],
            heading="Cards"
        ),
        FieldPanel("services_home_page"),
        FieldPanel("first_time_visitors_page"),
        FieldPanel("display_next_events"),
    ]

    upcoming_events_last_checked = models.DateTimeField(default=timezone.make_aware(timezone.datetime.min))
    upcoming_events = models.BinaryField(null=True)  # Pickled Events

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['upcoming_events'] = self.get_upcoming_events(request)
        next_oos = (
            OrderOfService.objects.filter(date__gte=timezone.now())
            .order_by('date')
            .first()
        )
        if next_oos:
            context['next_service'] = next_oos.service.specific
        return context

    def get_upcoming_events(self, request):
        site_settings = SiteWideSettings.load()
        if (timezone.now()
            - self.upcoming_events_last_checked) \
                > datetime.timedelta(minutes=site_settings.refresh_from_planningcenter_every):
            pco = pypco.PCO(settings.PLANNING_CENTER_APPLICATION_ID, settings.PLANNING_CENTER_SECRET)
            upcoming_event_instances = pco.get(
                '/calendar/v2/event_instances',
                order='starts_at',
                include='event',
                filter='future',
            )
            output_events = []
            print('gettingevents')
            for index, event_instance in enumerate(upcoming_event_instances['data'], start=0):
                event = pco.get(
                    event_instance['relationships']['event']['links']['related']
                )
                if event['data']['attributes']['visible_in_church_center']:
                    if len(output_events) >= self.display_next_events:
                        break
                    output_events.append(Event(
                        name=event['data']['attributes']['name'],
                        start_time=timezone.localtime(
                            parse_datetime(
                                event_instance['attributes']['starts_at']
                            )
                        ),
                        end_time=timezone.localtime(
                            parse_datetime(
                                event_instance['attributes']['ends_at']
                            )
                        ),
                        link=f'https://uucb.churchcenter.com/calendar/event/{event_instance["id"]}'
                    ))
            self.upcoming_events = pickle.dumps(output_events)
            self.upcoming_events_last_checked = timezone.now()
            self.save()
            return output_events
        else:
            return pickle.loads(self.upcoming_events)

    def get_carousel_image(self):
        return random.choice(self.carousel_images.all())

    def get_placeholder_upcoming_events(self):  # Generate some placeholder events for now. Eventually, this will somehow pull from PC
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