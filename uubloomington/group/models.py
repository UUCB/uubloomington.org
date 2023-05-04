import datetime

import pypco
from django.db import models

from django.conf import settings
from modelcluster.fields import ParentalKey
from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField
from django.db.models import CharField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel

from core.models import Post

class GroupsHomePage(Page):
    body = RichTextField()
    parent_page_types = ['home.HomePage']
    content_panels = Page.content_panels + [
        FieldPanel('body')
    ]


class GroupPage(Page):
    planning_center_group_id = models.CharField(max_length=20)
    show_posts = models.BooleanField(default=True)
    content_panels = Page.content_panels + [
        FieldPanel('planning_center_group_id'),
        FieldPanel('show_posts'),
    ]

    def group_info(self):
        planningcenter = pypco.PCO(settings.PLANNING_CENTER_APPLICATION_ID, settings.PLANNING_CENTER_SECRET)
        group = planningcenter.get(f'https://api.planningcenteronline.com/groups/v2/groups/{self.planning_center_group_id}')
        return group

    def get_posts(self):
        return self.get_children().type(Post)