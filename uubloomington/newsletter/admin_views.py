from .models import Issue, Newsletter
from core.models import Post
from django.utils import timezone
from django.shortcuts import HttpResponseRedirect, reverse


def create_issue(request, parent_page):
    issue = Issue.objects.create(
        title = f"{parent_page.title} for {timezone.now()}"
    )
    for post in Post.objects.filter(publish_in_newsletter=parent_page):
        issue.posts.add(post)
    issue.save()
    return HttpResponseRedirect(reverse('wagtailadmin_pages:edit', issue.id))