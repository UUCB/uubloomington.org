import datetime

import pypco
from django.db import models

from django.conf import settings
from modelcluster.fields import ParentalKey
from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField
from django.db.models import CharField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.images.edit_handlers import ImageChooserPanel


class GroupsHomePage(Page):
    pass

class GroupPage(Page):
    planning_center_group_id = models.CharField(max_length=20)
    content_panels = Page.content_panels + [
        FieldPanel('planning_center_group_id'),
    ]

    def group_info(self):
        planningcenter = pypco.PCO(settings.PLANNING_CENTER_APPLICATION_ID, settings.PLANNING_CENTER_SECRET)
        return planningcenter.get(f'https://api.planningcenteronline.com/groups/v2/groups/{self.planning_center_group_id}')
