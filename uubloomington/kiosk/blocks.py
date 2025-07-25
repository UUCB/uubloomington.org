from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.blocks import StructBlock
from wagtail_color_panel.blocks import NativeColorBlock
from core.blocks import *
from planningcenter_events.blocks import EventListingBlock
from planningcenter_events.models import EventListing


class KioskSidebarContentBlock(StructBlock):
    title = blocks.CharBlock(required=False)
    featured_image = ImageChooserBlock(required=False)
    body = blocks.StreamBlock(
        [
            ('rich_text', blocks.RichTextBlock()),
            ('image', ImageChooserBlock()),
        ],
    )

    def get_template(self, value=None, context=None):
        return "kiosk/blocks/kiosk_sidebar_content.html"

class KioskContentBlock(StructBlock):
    title = blocks.CharBlock()
    featured_image = ImageChooserBlock()
    one_sentence = blocks.RichTextBlock(
        help_text="Shown on the kiosk front page.",
    )
    details = blocks.StreamBlock(
        [
            ('rich_text', blocks.RichTextBlock()),
            ('read_more', ReadMoreTagBlock()),
            ('show_featured_image', ShowFeaturedImageBlock()),
            ('page_feature', PageFeatureBlock()),
            ('expandable_list', blocks.ListBlock(ExpandableListItemBlock)),
            ('embed', EmbedBlock(max_height=900)),
            ('auto_index', AutoIndexBlock()),
            ('selectable_index', IndexBlock()),
            ('document_list', DocumentListBlock()),
            ('badge_area', BadgeAreaBlock(BadgeBlock())),
            ('anchor', AnchorBlock()),
            ('upcoming_service', UpcomingServiceBlock()),
            ('upcoming_oos', UpcomingOrderOfServiceBlock()),
            ('multi_column', MultiColumnBlock()),
            ('directions', DirectionsBlock()),
            ('page_tree_index', SearchableTreeIndexBlock()),
            ('advanced_form', AdvancedFormBlock(AdvancedForm)),
            ('card_container', CardContainerBlock()),
            ('section', SectionBlock()),
            ('table_of_contents', TableOfContentsBlock()),
            ('event_listing', EventListingBlock(EventListing)),
        ],
        help_text="Shown when this content is selected on the kiosk",
    )
    details_page = blocks.PageChooserBlock(
        help_text="If not empty, overrides the Details field with the body of the selected page",
        required=False,
    )
    accent_color = NativeColorBlock(
        help_text="Accent color for this content. Primarily used for borders.",
        default="#006b1b",
    )

    def get_template(self, value=None, context=None):
        return "kiosk/blocks/kiosk_content.html"
    class Meta:
        collapsed = True
