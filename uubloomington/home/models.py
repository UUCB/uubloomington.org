import datetime
import random
import pickle

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
    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [InlinePanel("carousel_images", min_num=1, label="Image")],
            heading="Carousel Images",
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
    ]

    upcoming_events_last_checked = models.DateTimeField(default=timezone.make_aware(timezone.datetime.min))
    upcoming_events = models.BinaryField(null=True)  # Pickled Events
    live_stream_page = models.ForeignKey(
        to=Page,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

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

    def get_start_and_end(self, pco, times_url):
        """
        :param pco:
        Instance of pypco.PCO to use for API requests
        :param times_url:
        URL to the event_times endpoint for an event_instance in the Planning Center API
        :return:
        Two-item list of start time and end time
        """
        event_times = pco.get(times_url)
        for time in event_times['data']:
            if time['attributes']['visible_on_kiosks']:
                times = (
                    parse_datetime(time['attributes']['starts_at']),
                    parse_datetime(time['attributes']['ends_at']),
                )
            else:
                times = None
            return times

    def get_upcoming_events(self, request):
        site_settings = SiteWideSettings.load()
        if request.GET.get("refreshevents") == 'true':
            pco = pypco.PCO(settings.PLANNING_CENTER_APPLICATION_ID, settings.PLANNING_CENTER_SECRET)
            upcoming_event_instances = pco.get(
                '/calendar/v2/event_instances',
                order='starts_at',
                include='event',
                filter='future',
            )
            output_events = []
            for index, event_instance in enumerate(upcoming_event_instances['data'], start=0):
                event = pco.get(
                    event_instance['relationships']['event']['links']['related']
                )
                times = self.get_start_and_end(pco, f"{event_instance['links']['self']}/event_times")
                if not times:
                    continue  # Don't throw a 500 error if the event is visible on Church Center but has no public times
                if event['data']['attributes']['visible_in_church_center']:
                    if len(output_events) >= self.display_next_events:
                        break
                    output_events.append(Event(
                        name=event['data']['attributes']['name'],
                        start_time=timezone.localtime(times[0]),
                        end_time=timezone.localtime(times[1]),
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


class Event():  # Eventually, this should be replaced with an external module
    def __init__(self, name:str, link:str, start_time:datetime.datetime, end_time:datetime.datetime):
        self.name = name
        self.link = link
        self.start_time = start_time
        self.end_time = end_time

    def readable_times(self):
        return {
            'date': self.start_time.strftime('%A, %B %-d'),
            'start_time': self.start_time.strftime('%-I:%M %p'),
            'end_time': self.end_time.strftime('%-I:%M %p'),
        }