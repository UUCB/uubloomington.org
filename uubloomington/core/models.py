from django.db import models
from wagtail.models import Page, Orderable
from modelcluster.fields import ParentalKey
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, PageChooserPanel, MultiFieldPanel, InlinePanel
from wagtail import blocks
from wagtail.embeds.blocks import EmbedBlock
from .blocks import ReadMoreTagBlock, ShowFeaturedImageBlock, PageFeatureBlock, ExpandableListItemBlock


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
    ], use_json_field=True, null=True)

    content_panels = Page.content_panels + [
        FieldPanel('featured_image'),
        FieldPanel('body'),
    ]
