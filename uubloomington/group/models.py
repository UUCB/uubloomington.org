import datetime

import pypco
from django.db import models

from django.conf import settings
from modelcluster.fields import ParentalKey
from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField
from django.db.models import CharField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from django.utils.text import slugify
from django.utils import timezone

from site_settings.models import SiteWideSettings

from core.models import Post

import pickle

class GroupsHomePage(Page):
    body = RichTextField()
    featured_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    parent_page_types = ['home.HomePage']
    content_panels = Page.content_panels + [
        FieldPanel('body'),
        FieldPanel('featured_image'),
    ]


class GroupPage(Page):
    planning_center_group_id = models.CharField(max_length=20)
    show_posts = models.BooleanField(default=True)
    summary = RichTextField(null=True, blank=True)
    featured_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    group_info = models.BinaryField(null=True)  # Pickled Group
    group_type = models.BinaryField(null=True)  # Pickled Group Type
    last_fetched = models.DateTimeField(default=timezone.make_aware(datetime.datetime.min))
    content_panels = Page.content_panels + [
        FieldPanel('planning_center_group_id'),
        FieldPanel('summary'),
        FieldPanel('featured_image'),
        FieldPanel('show_posts'),
    ]

    def get_context(self, request, *args, **kwargs):
        site_settings = SiteWideSettings.load()
        context = super().get_context(request)
        if self.last_fetched < (
            timezone.now()
            - datetime.timedelta(minutes=site_settings.refresh_from_planningcenter_every)
        ):
            planningcenter = pypco.PCO(settings.PLANNING_CENTER_APPLICATION_ID, settings.PLANNING_CENTER_SECRET)
            group_info = planningcenter.get(f'https://api.planningcenteronline.com/groups/v2/groups/{self.planning_center_group_id}')
            group_type = planningcenter.get(f'https://api.planningcenteronline.com/groups/v2/group_types/{group_info["data"]["relationships"]["group_type"]["data"]["id"]}')
            self.group_info = pickle.dumps(group_info)
            self.group_type = pickle.dumps(group_type)
            self.save()
        else:
            group_info = pickle.loads(self.group_info)
            group_type = pickle.loads(self.group_type)
        context['group'] = group_info
        context['group_title'] = group_info['data']['attributes']['name']
        context['group_body'] = group_info['data']['attributes']['description']
        context['header_image'] = group_info['data']['attributes']['header_image']['original']
        group_type_slug = slugify(group_type['data']['attributes']['name'])
        group_slug = slugify(context['group_title'])
        # TODO: Add a setting for churchcenter base URL and un-hard-code this
        context['churchcenter_group_url'] = f'https://uucb.churchcenter.com/groups/{group_type_slug}/{group_slug}/'
        return context

    def get_posts(self):
        return self.get_children().type(Post)