from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, PageChooserPanel, MultiFieldPanel, InlinePanel
from wagtail.admin.forms import WagtailAdminPageForm
from wagtail.admin.views.pages.create import CreateView
from wagtail import hooks

import datetime

from recurrence.fields import RecurrenceField

from recurrence.forms import RecurrenceWidget

from core.models import Post

from django.utils import timezone
from django.shortcuts import HttpResponseRedirect, reverse

# from .admin_views import create_issue


class Newsletter(Page):
    description = RichTextField()
    publication_schedule = RecurrenceField()

    content_panels = Page.content_panels + [
        FieldPanel('description'),
        FieldPanel('publication_schedule'),
    ]

    def get_posts_for_new_issue(self):
        return Post.objects.filter()

    def get_date_of_next_issue(self):
        existing_issues = [issue.specific.publication_date for issue in self.get_children()]
        existing_issues.append(datetime.datetime.now().date())  # Don't break if there are no existing issues.
        # Using now() for this is fine, as we should never create any issues that are in the past anyway.
        latest_issue_date = max(existing_issues)
        latest_issue_datetime = datetime.datetime.combine(latest_issue_date, datetime.time.min)
        print(f'Latest:{latest_issue_date}')
        return self.publication_schedule.after(latest_issue_datetime, dtstart=latest_issue_datetime, inc=False).date()

class Issue(Page):
    # newsletter = models.ForeignKey(
    #     to=Newsletter,
    #     null=True,
    #     blank=False,
    #     on_delete=models.CASCADE,
    #     related_name="issues",
    # )
    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [InlinePanel("segments", label="Segment")],
            heading="Segments",
        )
    ]
    publication_date = models.DateField()


    # def save(self, *args, **kwargs):
    #     self.newsletter = self.get_parent()
    #     super(Issue, self).save(*args, **kwargs)


class IssueSegment(Orderable):
    issue = ParentalKey("newsletter.Issue", related_name="segments")
    post = models.ForeignKey(
        "core.Post",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    panels = [
        PageChooserPanel("post", "core.Post")
    ]


class CreateIssueView(CreateView):
    def get(self, request):
        pass


@hooks.register('before_create_page')
def before_create_issue(request, parent_page, page_class):
    if page_class == Issue:
        issue = Issue(
            title=f"{parent_page.title} for {parent_page.get_date_of_next_issue()}",
            publication_date=parent_page.get_date_of_next_issue(),
        )
        parent_page.add_child(instance=issue)
        for post in Post.objects.filter(
                publish_in_newsletter=parent_page,
                intended_publication__range=[
                    issue.get_parent().get_children().order_by('id').reverse()[1].specific.publication_date,
                    issue.publication_date
                ],
        ):
            segment = IssueSegment(issue=issue, post=post)
            segment.save()
        issue.save()
        return HttpResponseRedirect(reverse('wagtailadmin_pages:edit', args={issue.id}))

