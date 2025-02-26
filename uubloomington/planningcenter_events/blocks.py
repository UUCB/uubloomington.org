from wagtail.snippets.blocks import SnippetChooserBlock
from planningcenter_events.models import EventListing


class EventListingBlock(SnippetChooserBlock):
    model = EventListing

    class Meta:
        template = 'planningcenter_events/blocks/event_listing.html'
