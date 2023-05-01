import datetime

from django.db import models

from django.dispatch import receiver
from django.db.models.signals import post_save

from modelcluster.fields import ParentalKey
from wagtail.models import Page, Orderable, Site
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.contrib import settings
from site_settings.models import SiteWideSettings

from recurrence.fields import RecurrenceField

from wagtail.blocks import RichTextBlock
from .blocks import OOSElementBlock, OOSMultiColumnBlock


def get_default_stream_url():
    return SiteWideSettings.load().livestream_url


class ServicesHomePage(Page):
    body = RichTextField(blank=True, null=True)
    service_schedule = RecurrenceField(blank=False, null=True)
    service_time = models.TimeField(blank=False, null=True)
    content_panels = Page.content_panels + [
        FieldPanel('body'),
        MultiFieldPanel(
            [
                FieldPanel('service_schedule', heading="Services happen every:"),
                FieldPanel('service_time', heading="At:"),
            ],
            heading="Service Schedule"
        )
    ]


    def get_next_service_time(self):
        existing_services = [service.specific.order_of_service.first().date for service in self.get_children() if service.specific.order_of_service.first()]
        existing_services.append(datetime.datetime.now().date())  # Don't break if there are no existing services.
        # Using now() for this is fine, as we should never create any services that are in the past anyway.
        latest_service_date = max(existing_services)
        latest_service_datetime = datetime.datetime.combine(latest_service_date, datetime.time.min)
        return self.service_schedule.after(latest_service_datetime, dtstart=latest_service_datetime, inc=False).date()


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


    def get_context(self, request):
        context = super().get_context(request)
        servicepages = self.get_siblings().live().order_by('-title')
        context['servicepages'] = servicepages
        return context


class Participant(Orderable):
    # copy_from = models.ForeignKey(unique=False)
    service = ParentalKey("services.ServicePage", related_name='participants')
    name = models.CharField(max_length=100, blank=True, null=False)
    bio = RichTextField(blank=True, null=True)

    panels = [
        FieldPanel('name'),
        FieldPanel('bio'),
    ]


class OrderOfService(Page):
    service = models.ForeignKey(
        to=ServicePage,
        null=False,
        blank=False,
        unique=True,
        on_delete=models.CASCADE,
        related_name='order_of_service',
    )
    # back_page = RichTextField()
    # front_page = RichTextField()
    date = models.DateField()
    time = models.TimeField()
    program = StreamField(
       [
           ('element', OOSElementBlock()),
           ('text', RichTextBlock()),
           ('multicolumn', OOSMultiColumnBlock()),
       ],
        null=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("program")
    ]


@receiver(post_save, sender=ServicePage)
def create_matching_order_of_service(sender, instance, **kwargs):
    service = instance
    previous_order_of_service = OrderOfService.objects.order_by("-date").first()
    if not service.order_of_service.first():
        next_service_date = service.get_parent().specific.get_next_service_time()
        order_of_service = OrderOfService(
            title=f"Order of Service for {next_service_date}",
            service=service,
            time=service.get_parent().specific.service_time,
            date=next_service_date,
            # front_page=previous_order_of_service.front_page,
            # back_page=previous_order_of_service.back_page,
        )
        service.add_child(instance=order_of_service)
        order_of_service.save()
        service.title = f"{str(order_of_service.date)}: {service.title}"
        service.save()


