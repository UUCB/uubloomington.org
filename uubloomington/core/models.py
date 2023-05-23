from django.db import models
from wagtail.models import Page, Orderable
from modelcluster.fields import ParentalKey
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, PageChooserPanel, MultiFieldPanel, InlinePanel
from wagtail import blocks
from .blocks import ReadMoreTagBlock


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


class ListPage(Page):
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
        MultiFieldPanel(
            [
                InlinePanel(
                    "list_items",
                    label="List Item"
                )
            ],
            heading="List Items",
        )
    ]


class ListPageItem(Orderable):
    page = ParentalKey(
        to=ListPage,
        related_name="list_items"
    )
    title = models.CharField(max_length=200)
    body = StreamField([
        ('text', blocks.RichTextBlock()),
        ('read_more', ReadMoreTagBlock()),
    ], use_json_field=True, null=True)
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    panels = [
        FieldPanel('image'),
        FieldPanel('title'),
        FieldPanel('body'),
    ]
