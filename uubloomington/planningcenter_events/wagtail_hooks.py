from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet
from wagtail.admin.panels import FieldPanel

from .models import EventListing


class EventListingViewSet(SnippetViewSet):
    model = EventListing
    panels = [
        FieldPanel('name'),
        FieldPanel('description_must_contain'),
        FieldPanel('show_next_events'),
    ]


register_snippet(EventListingViewSet)
