import datetime

import pypco
from django.db import models

from django.conf import settings
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from django.utils.text import slugify
from django.utils import timezone
from wagtail.search import index

from site_settings.models import SiteWideSettings

from core.models import Post

import pickle


def cc_slugify(value: str) -> str:
    """
    An attempt to recreate whatever Church Center uses for slugify() functionality.
    Replaces "/" and "'" with "-", then runs django.utils.text.slugify.
    :param value:
    String to be slugified
    :return:
    str
    """
    translate_table = str.maketrans("'/", "--")
    return slugify(value.translate(translate_table))


class GroupsHomePage(Page):
    body = RichTextField()
    featured_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    # parent_page_types = ['home.HomePage']
    content_panels = Page.content_panels + [
        FieldPanel('body'),
        FieldPanel('featured_image'),
    ]


class GroupPage(Page):
    planning_center_group_id = models.CharField(max_length=20)
    show_posts = models.BooleanField(default=True)
    summary = RichTextField(null=False, blank=True, default='')
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

    search_fields = Page.search_fields + [
        index.SearchField('summary'),

    ]

    def get_context(self, request, *args, **kwargs):
        site_settings = SiteWideSettings.load()
        context = super().get_context(request)
        if (self.last_fetched < (
            timezone.now()
            - datetime.timedelta(minutes=site_settings.refresh_from_planningcenter_every)
        )
                or request.GET.get('refresh') == "true")\
                or request.is_preview:
            planningcenter = pypco.PCO(settings.PLANNING_CENTER_APPLICATION_ID, settings.PLANNING_CENTER_SECRET)
            group_info = planningcenter.get(f'https://api.planningcenteronline.com/groups/v2/groups/{self.planning_center_group_id}')
            group_type = planningcenter.get(f'https://api.planningcenteronline.com/groups/v2/group_types/{group_info["data"]["relationships"]["group_type"]["data"]["id"]}')
            self.group_info = pickle.dumps(group_info)
            self.group_type = pickle.dumps(group_type)
            if not request.is_preview:
                self.last_fetched = timezone.now()
                self.save()
        else:
            group_info = pickle.loads(self.group_info)
            group_type = pickle.loads(self.group_type)
        if request.user.has_perm("wagtailadmin.access_admin"):
            context['refresh_from_planningcenter_link'] = True
        context['group'] = group_info
        context['group_title'] = group_info['data']['attributes']['name']
        context['group_body'] = group_info['data']['attributes']['description']
        context['header_image'] = group_info['data']['attributes']['header_image']['original']
        group_type_slug = cc_slugify(group_type['data']['attributes']['name'])
        group_slug = cc_slugify(context['group_title'])
        # TODO: Add a setting for churchcenter base URL and un-hard-code this
        context['churchcenter_group_url'] = f'https://uucb.churchcenter.com/groups/{group_type_slug}/{group_slug}/'
        return context

    def get_posts(self):
        return self.get_children().type(Post)