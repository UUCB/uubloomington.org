import pickle

from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.blocks import StructBlock
from wagtail_color_panel.blocks import NativeColorBlock
from core.blocks import *
from planningcenter_events.blocks import EventListingBlock
from planningcenter_events.models import EventListing
from group.models import cc_slugify

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
        required=False,
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

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        if context['value']['details_page'] and type(context['value']['details_page'].specific).__name__ == 'GroupPage':
            group_info = pickle.loads(value['details_page'].specific.group_info)
            group_type = pickle.loads(value['details_page'].specific.group_type)
            context['group'] = group_info
            context['group_title'] = group_info['data']['attributes']['name']
            context['group_body'] = group_info['data']['attributes']['description']
            context['header_image'] = group_info['data']['attributes']['header_image']['original']
            group_type_slug = cc_slugify(group_type['data']['attributes']['name'])
            group_slug = cc_slugify(context['group_title'])
            context['churchcenter_group_url'] = f'https://uucb.churchcenter.com/groups/{group_type_slug}/{group_slug}/'
        return context

    class Meta:
        collapsed = True
