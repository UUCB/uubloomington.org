import datetime

from django.db import models

from django.dispatch import receiver
from django.db.models.signals import post_save

from django.utils import timezone

from modelcluster.fields import ParentalKey
from wagtail.models import Page, Orderable, Site
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.images.models import Image
from wagtail.api import APIField

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

    subpage_types = ['services.ServicePage']

    def get_next_service_time(self):
        existing_services = [service.specific.order_of_service.first().date
                             for service in self.get_children()
                             if service.specific.order_of_service.first()]
        existing_services.append(datetime.datetime.now().date())  # Don't break if there are no existing services.
        # Using now() for this is fine, as we should never create any services that are in the past anyway.
        latest_service_date = max(existing_services)
        latest_service_datetime = datetime.datetime.combine(latest_service_date, datetime.time.min)
        return self.service_schedule.after(latest_service_datetime, dtstart=latest_service_datetime, inc=False).date()

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request)
        next_oos = (
            OrderOfService.objects.filter(date__gte=timezone.now())
            .order_by('date')
            .first()
        )
        if next_oos:
            context['next_service'] = next_oos.service.specific
        next_services = []
        for oos in OrderOfService.objects.filter(date__gte=timezone.now()).order_by('date'):
            if oos.service.live:
                next_services.append(oos.service)
            if len(next_services) > 8:
                break
        if len(next_services) > 0:
            next_services.pop(0)
        context['next_services_list'] = next_services
        previous_services = []
        previous_oos_list = OrderOfService.objects.filter(date__lte=timezone.now()).order_by('-date')
        for oos in previous_oos_list:
            if oos.service.live:
                previous_services.append(oos.service)
            if len(previous_services) > 5:
                break
        if previous_oos_list.count() > len(previous_services):
            context['show_expand_previous_services'] = True
        context['previous_services_list'] = previous_services
        if len(previous_services) > 0:
            context['last_previous_service'] = previous_services[-1]
        return context


class ServicePage(Page):
    body = RichTextField(blank=True, null=True)
    one_sentence = models.CharField(max_length=200, blank=False, null=True)
    vimeo_link = models.CharField(max_length=100, blank=False, null=True, default=get_default_stream_url)
    featured_image = models.ForeignKey(to=Image, on_delete=models.SET_NULL, null=True, blank=True)
    # order_of_service_link = models.CharField(max_length=900, blank=True, null=True)
    video_archive_link = models.CharField(max_length=400, blank=True, null=True)

    parent_page_types = ['ServicesHomePage']

    content_panels = Page.content_panels + [
        FieldPanel('body'),
        FieldPanel('one_sentence', heading='One-Sentence Description'),
        FieldPanel('featured_image'),
        MultiFieldPanel(
            [InlinePanel('participants', label="Participant")],
            heading="Participants"
        ),
        FieldPanel('video_archive_link'),
        # FieldPanel('order_of_service_link'),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request)
        service_pages = self.get_siblings().live().order_by('-title')
        context['service_pages'] = service_pages
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
        on_delete=models.PROTECT,
        unique=True,
        related_name='order_of_service',
    )
    back_page = RichTextField(null=True, blank=True)
    cover_page = RichTextField(null=True, blank=True)
    date = models.DateField()
    time = models.TimeField()
    program = StreamField(
        [
           ('element', OOSElementBlock()),
           ('text', RichTextBlock()),
           ('multicolumn', OOSMultiColumnBlock()),
        ],
        null=True,
        use_json_field=True,
    )

    parent_page_types = ['services.ServicePage']
    subpage_types = []
    max_count_per_parent = 1

    content_panels = Page.content_panels + [
        FieldPanel("program"),
        FieldPanel("cover_page"),
        FieldPanel("back_page"),
    ]

    api_fields = [
        APIField('program'),
        APIField('date'),
    ]

    def get_readable_date(self):
        return f'{self.date.strftime("%B %d, %Y")}'

    def get_readable_time(self):
        return f'{self.time.strftime("%I:%M %p")}'

    def get_template(self, request, *args, **kwargs):
        print(request.GET)
        if request.GET.get("print") == 'true':
            return 'services/order_of_service_print.html'
        return 'services/order_of_service.html'


@receiver(post_save, sender=ServicePage)
def create_matching_order_of_service(sender, instance, **kwargs):
    service = instance.specific
    previous_order_of_service = OrderOfService.objects.order_by("-date").first()
    if not service.order_of_service.first():
        next_service_date = service.get_parent().specific.get_next_service_time()
        order_of_service = OrderOfService(
            title=f"Order of Service for {next_service_date}",
            service=service,
            program=previous_order_of_service.program,
            time=service.get_parent().specific.service_time,
            date=next_service_date,
            live=False,
            # front_page=previous_order_of_service.front_page,
            # back_page=previous_order_of_service.back_page,
        )
        service.add_child(instance=order_of_service)
        service.title = f"{str(order_of_service.get_readable_date())}: {service.title}"
        service.save_revision()


