import datetime

from django.db import models

from django.dispatch import receiver
from django.db.models.signals import post_save
from django.shortcuts import redirect

from django.utils import timezone
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, TabbedInterface, ObjectList
from wagtail.images.models import Image
from wagtail.api import APIField
from wagtail.search import index

from site_settings.models import SiteWideSettings

from recurrence.fields import RecurrenceField

from wagtail.blocks import RichTextBlock
from .blocks import OOSElementBlock, OOSMultiColumnBlock


def get_default_stream_url():
    return SiteWideSettings.load().livestream_url


class ServicesHomePage(Page):
    body = RichTextField(blank=True, null=True)
    service_schedule = RecurrenceField(blank=False, null=True)
    services_per_page = models.IntegerField(
        default=15,
        verbose_name="Services per Page",
        help_text="Display this many archived services per page.",
    )
    service_archive_start = models.DateField(
        default=datetime.date.min,
        verbose_name="Service Archive Start Date",
        help_text="Don't show any services older than this date in the paginated archive.",
    )
    order_of_service_program_template = StreamField(
        [
           ('element', OOSElementBlock()),
           ('text', RichTextBlock()),
           ('multicolumn', OOSMultiColumnBlock()),
        ],
        null=True,
        use_json_field=True,
        verbose_name="Order of Service Program Template",
        help_text="Newly-created Order of Service pages will contain this in their Program field."
    )

    order_of_service_panels = [
        FieldPanel('order_of_service_program_template'),
    ]

    preview_modes = []  # Disable preview for this page type as there are no editing options

    content_panels = Page.content_panels + [
        FieldPanel('body'),
        MultiFieldPanel(
            [
                FieldPanel('service_schedule', heading="Services happen every:"),
            ],
            heading="Service Schedule"
        )
    ]

    archive_panels = [
        FieldPanel('services_per_page'),
        FieldPanel('service_archive_start'),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading="Content"),
        ObjectList(order_of_service_panels, heading="Order of Service Program Template"),
        ObjectList(archive_panels, heading="Archive"),
        ObjectList(Page.promote_panels, heading="Promote"),
    ])

    subpage_types = ['services.ServicePage']

    search_fields = Page.search_fields + [
        index.SearchField('body'),
    ]

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
        next_services = ServicePage.objects.filter(
            order_of_service__date__gte=timezone.now(),
            live=True,
        ).order_by('order_of_service__date')
        context['next_service'] = next_services.first()
        context['next_services_list'] = next_services[1:8]
        all_previous_services = ServicePage.objects.filter(
            order_of_service__date__gte=self.service_archive_start,
            order_of_service__date__lte=timezone.now(),
            live=True,
        ).order_by('-order_of_service__date')
        previous_services_paginator = Paginator(all_previous_services, self.services_per_page)
        page = request.GET.get('page')
        try:
            displayed_previous_services = previous_services_paginator.page(page)
        except PageNotAnInteger:
            displayed_previous_services = previous_services_paginator.page(1)
        except EmptyPage:
            displayed_previous_services = previous_services_paginator.page(previous_services_paginator.num_pages)
        context['previous_services_list'] = displayed_previous_services
        return context


class ServicePage(Page):
    body = RichTextField(blank=False, null=True)
    short_description = RichTextField(
        blank=False,
        null=True,
        verbose_name="Short Description",
        help_text="A shortened description of the service, displayed on the home page. "
                  "Needs to be extremely short when also using a featured image.",
    )
    featured_image = models.ForeignKey(to=Image, on_delete=models.SET_NULL, null=True, blank=True)
    video_archive_link = models.CharField(max_length=400, blank=True, null=True)
    show_video_embed = models.BooleanField(default=True)
    transcript_heading = models.CharField(max_length=200, default="Sermon Text")
    transcript = RichTextField(blank=True, null=True)
    homepage_location_text = models.CharField(max_length=200, blank=False, null=False, default='or in person!')

    parent_page_types = ['ServicesHomePage']

    content_panels = Page.content_panels + [
        FieldPanel('featured_image'),
        FieldPanel('body'),
        FieldPanel('short_description'),
        FieldPanel('homepage_location_text'),
    ]

    archive_panels = [
        FieldPanel('video_archive_link'),
        FieldPanel('show_video_embed'),
    ]

    transcript_panels = [
        FieldPanel('transcript_heading'),
        FieldPanel('transcript'),
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading="Content"),
            ObjectList(archive_panels, heading="Archive"),
            ObjectList(transcript_panels, heading="Transcript"),
            ObjectList(Page.promote_panels, heading="Promote"),
        ]
    )

    search_fields = Page.search_fields + [
        index.SearchField('body'),
        index.SearchField('short_description'),
        index.SearchField('transcript'),
    ]

    def service_in_future(self):
        oos = self.get_children().first()
        result = False
        if not oos:
            result = True
        elif oos and timezone.now().date() <= oos.specific.date:
            result = True
        else:
            result = False
        return result

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request)
        next_services = ServicePage.objects.filter(
            order_of_service__date__gte=timezone.now(),
            live=True,
        ).order_by('order_of_service__date')
        context['next_services'] = next_services
        return context


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
    back_page_title = models.CharField(
        max_length=255,
        blank=False,
        default="Other Sunday Information",
        help_text="This will be the title of the \"back page\" tab on the service page.",
    )
    back_page_description = RichTextField(
        default='Information about other happenings at UUCB each week is available here.',
        help_text="This will be the short description of the \"back page\" tab on the service page, displayed just under the title.",
        blank=False,
    )
    cover_page = RichTextField(null=True, blank=True)
    date = models.DateField()
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

    program_panels = Page.content_panels + [
        FieldPanel("program"),
        FieldPanel("date"),
    ]

    cover_page_panels = [
        FieldPanel("cover_page")
    ]

    back_page_panels = [
        FieldPanel("back_page_title"),
        FieldPanel("back_page_description"),
        FieldPanel("back_page"),
    ]

    edit_handler = TabbedInterface([
        ObjectList(program_panels, heading="Program"),
        # ObjectList(cover_page_panels, heading="Cover Page"),
        # We're not using this right now; it is only displayed in the (unfinished) print template.
        # Uncomment this ObjectList if we ever decide to use that functionality.
        ObjectList(back_page_panels, heading="Back Page"),
        ObjectList(Page.promote_panels, heading="Promote"),
    ])

    api_fields = [
        APIField('program'),
        APIField('date'),
    ]

    search_fields = Page.search_fields + [
        index.SearchField('program'),
    ]

    def is_on_sunday(self):
        if self.date.strftime("%A") == 'Sunday':
            return True
        else:
            return False

    def get_readable_date(self):
        return f'{self.date.strftime("%B %-d, %Y")}'

    def get_template(self, request, *args, **kwargs):
        if request.GET.get("print") == 'true':
            return 'services/order_of_service_print.html'
        return 'services/order_of_service.html'

    def save_revision(self, *args, **kwargs):
        if self.pk:
            cls = self.__class__
            old = cls.objects.get(pk=self.pk)
            if old.date != self.date:
                self.title = f"Order of Service for {self.date}"
                service_title = self.service.title
                index = service_title.find(':')
                self.service.title = f'{self.get_readable_date()}{service_title[index:]}'
                service = self.service.save_revision()
                if self.service.live:
                    self.service.publish(service)
        return super(OrderOfService, self).save_revision(*args, **kwargs)

    def serve(self, request, *args, **kwargs):
        if request.GET.get("print") == 'true':
            return super(OrderOfService, self).serve(request, *args, **kwargs)
        else:
            return redirect(self.get_parent().url, permanent=False)


@receiver(post_save, sender=ServicePage)
def create_matching_order_of_service(sender, instance, **kwargs):
    service = instance.specific
    if not service.order_of_service.first():
        next_service_date = service.get_parent().specific.get_next_service_time()
        order_of_service = OrderOfService(
            title=f"Order of Service for {next_service_date}",
            service=service,
            program=service.get_parent().specific.order_of_service_program_template,
            date=next_service_date,
            live=False,
        )
        service.add_child(instance=order_of_service)
        service.title = f"{str(order_of_service.get_readable_date())}: {service.title}"
        service.save_revision()


