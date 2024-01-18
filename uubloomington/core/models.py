from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, PageChooserPanel
from wagtail import blocks
from wagtail.embeds.blocks import EmbedBlock
from .blocks import ReadMoreTagBlock, ShowFeaturedImageBlock, PageFeatureBlock, ExpandableListItemBlock, AutoIndexBlock, IndexBlock, DocumentListBlock, BadgeAreaBlock, BadgeBlock, AnchorBlock, UpcomingServiceBlock, MultiColumnBlock, UpcomingOrderOfServiceBlock
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import (
    FieldPanel, FieldRowPanel,
    InlinePanel, MultiFieldPanel
)
from wagtail.fields import RichTextField
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.contrib.forms.panels import FormSubmissionsPanel


class Post(Page):
    body = RichTextField()
    featured_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    publish_in_newsletter = models.ForeignKey(
        "newsletter.Newsletter",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )

    intended_publication = models.DateField()

    content_panels = Page.content_panels + [
        FieldPanel('featured_image'),
        FieldPanel('body'),
        PageChooserPanel('publish_in_newsletter', page_type='newsletter.Newsletter'),
        FieldPanel('intended_publication'),
    ]


class PageWithPosts(Page):
    body = RichTextField()
    featured_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    show_posts = models.BooleanField(default=True)

    content_panels = Page.content_panels + [
        FieldPanel('featured_image'),
        FieldPanel('body'),
        FieldPanel('show_posts'),
    ]

    subpage_types = ['core.Post']


class GenericIndexPage(Page):
    body = RichTextField()
    featured_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    content_panels = Page.content_panels + [
        FieldPanel('featured_image'),
        FieldPanel('body'),
    ]


class StandardBlockPage(Page):
    featured_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    body = StreamField([
        ('rich_text', blocks.RichTextBlock()),
        ('read_more', ReadMoreTagBlock()),
        ('show_featured_image', ShowFeaturedImageBlock()),
        ('page_feature', PageFeatureBlock()),
        ('expandable_list', blocks.ListBlock(ExpandableListItemBlock)),
        ('embed', EmbedBlock(max_height=900)),
        ('auto_index', AutoIndexBlock()),
        ('selectable_index', IndexBlock()),
        ('document_list', DocumentListBlock()),
        ('badge_area', BadgeAreaBlock(child_block=BadgeBlock())),
        ('anchor', AnchorBlock()),
        ('upcoming_service', UpcomingServiceBlock()),
        ('upcoming_oos', UpcomingOrderOfServiceBlock()),
        ('multi_column', MultiColumnBlock()),
    ], use_json_field=True, null=True)

    body_is_streamfield = True

    content_panels = Page.content_panels + [
        FieldPanel('featured_image'),
        FieldPanel('body'),
    ]


class FormField(AbstractFormField):
    page = ParentalKey('FormPage', on_delete=models.CASCADE, related_name='form_fields')


class FormPage(AbstractEmailForm):
    intro = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)
    featured_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    content_panels = AbstractEmailForm.content_panels + [
        # FormSubmissionsPanel(),  # Can't use this until wagtail 5.2.3 https://github.com/wagtail/wagtail/issues/11405
        FieldPanel('featured_image'),
        FieldPanel('intro'),
        InlinePanel('form_fields', label="Form fields"),
        FieldPanel('thank_you_text'),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject'),
        ], "Email"),
    ]
