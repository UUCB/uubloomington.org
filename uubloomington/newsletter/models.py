from django.db import models
from wagtail.models import Page, StreamField
from wagtail.admin.panels import FieldPanel, HelpPanel
from wagtail.admin.views.pages.create import CreateView
from wagtail import hooks
from wagtail import blocks
from wagtail.embeds.blocks import EmbedBlock
from core.blocks import ReadMoreTagBlock, ShowFeaturedImageBlock, PageFeatureBlock, ExpandableListItemBlock, IndexBlock, BadgeAreaBlock, BadgeBlock, AnchorBlock
from core.models import StandardBlockPage
from .blocks import ArticleBlock, TableOfContentsBlock

import datetime

from recurrence.fields import RecurrenceField

from django.shortcuts import HttpResponseRedirect, reverse


class Newsletter(Page):
    body = StreamField([
        ('rich_text', blocks.RichTextBlock()),
        ('read_more', ReadMoreTagBlock()),
        ('show_featured_image', ShowFeaturedImageBlock()),
        ('page_feature', PageFeatureBlock()),
        ('expandable_list', blocks.ListBlock(ExpandableListItemBlock)),
        ('embed', EmbedBlock(max_height=900)),
        ('selectable_index', IndexBlock()),
        ('badge_area', BadgeAreaBlock(child_block=BadgeBlock())),
        ('anchor', AnchorBlock()),
    ], use_json_field=True, null=True)
    publication_schedule = RecurrenceField()
    content_panels = Page.content_panels + [
        FieldPanel('body'),
        FieldPanel('publication_schedule'),
    ]
    subpage_types = [
        'newsletter.Issue'
    ]

    def get_date_of_next_issue(self) -> datetime.date:
        existing_issues = [issue.specific.publication_date for issue in self.get_children()]
        existing_issues.append(datetime.datetime.now().date())  # Don't break if there are no existing issues.
        # Using now() for this is fine, as we should never create any issues that are in the past anyway.
        latest_issue_date = max(existing_issues)
        latest_issue_datetime = datetime.datetime.combine(latest_issue_date, datetime.time.min)
        print(f'Latest:{latest_issue_date}')
        return self.publication_schedule.after(latest_issue_datetime, dtstart=latest_issue_datetime, inc=False).date()

    template = 'core/standard_block_page.html'


class Issue(Page):
    featured_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    body = StreamField(
        [
            ('rich_text', blocks.RichTextBlock()),
            ('read_more', ReadMoreTagBlock()),
            ('show_featured_image', ShowFeaturedImageBlock()),
            ('page_feature', PageFeatureBlock()),
            ('expandable_list', blocks.ListBlock(ExpandableListItemBlock)),
            ('embed', EmbedBlock(max_height=900)),
            ('selectable_index', IndexBlock()),
            ('badge_area', BadgeAreaBlock(child_block=BadgeBlock())),
            ('anchor', AnchorBlock()),
            ('article', ArticleBlock()),
            ('table_of_contents', TableOfContentsBlock()),
        ],
        default=[
            ('show_featured_image',None),
            ('table_of_contents',None),
        ],
        use_json_field=True,
        null=True,
        blank=True,
    )
    content_panels = Page.content_panels + [
        HelpPanel(
            template='newsletter/admin/mailchimp_export.html'
        ),
        FieldPanel('featured_image'),
        FieldPanel('body'),
    ]
    parent_page_types = [
        'newsletter.Newsletter',
    ]
    subpage_types = [
        'newsletter.Article',
    ]
    publication_date = models.DateField()
    template = 'core/standard_block_page.html'

    newsletter = True  # for page feature handling

    def get_article_blocks(self):
        return [ block for block in self.body if block.block_type == 'article' ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['article_blocks'] = self.get_article_blocks()
        context['full_path'] = request.get_full_path().split('?')[0]
        return context

    def get_template(self, request, *args, **kwargs):
        if request.GET.get("mailchimp") == 'true':
            return 'newsletter/mailchimp_export.html'
        else:
            return super().get_template(request, *args, **kwargs)


class CreateIssueView(CreateView):
    def get(self, request):
        pass


@hooks.register('before_create_page')
def before_create_issue(request, parent_page, page_class):
    if page_class == Issue:
        publication_date = parent_page.get_date_of_next_issue(),
        issue = Issue(
            title=f"{parent_page.title} for {publication_date[0].strftime('%B %Y')}",  # TODO: Fix this so the day of the month is added when the newsletter is published more than monthly
            publication_date=publication_date[0],
        )
        parent_page.add_child(instance=issue)
        issue.save()
        return HttpResponseRedirect(reverse('wagtailadmin_pages:edit', args={issue.id}))


class Article(StandardBlockPage):
    parent_page_types = [
        'newsletter.Issue'
    ]
    template = 'newsletter/article.html'


