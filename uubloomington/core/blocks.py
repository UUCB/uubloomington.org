from tokenize import blank_re

from wagtail import blocks
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.snippets.blocks import SnippetChooserBlock
from wagtail.documents.models import Document

from advanced_forms.models import AdvancedForm
from services.models import OrderOfService
from django.utils import timezone


class ReadMoreTagBlock(blocks.StaticBlock):
    class Meta:
        icon = 'arrow-down'
        label = '"Read More" tag'
        admin_text = f'{label}: Anything after this tag will be hidden behind a "Read More" button.'
        template = 'core/read_more_snippet.html'


class DocumentListBlock(blocks.CharBlock):
    class Meta:
        required = True
        max_length = 200
        help_text = 'Display all documents with this tag'  # TODO: Make this help text actually appear in admin
        template = 'core/document_list_block.html'

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context)
        config = value.split(',')
        if len(config) < 2:
            config.append('-title')
        context['documents'] = Document.objects.filter(tags__name=config[0]).order_by(config[1])
        return context


class ShowFeaturedImageBlock(blocks.StaticBlock):
    class Meta:
        icon = 'image'
        label = 'Show Featured Image Here'
        admin_text = f'{label}: This is where the featured image will be shown.'
        template = 'core/show_featured_image_snippet.html'


class PageFeatureBlock(blocks.PageChooserBlock):
    class Meta:
        icon = 'page'
        label = 'Feature Another Page'
        admin_text = 'Anything before the "read more" tag on the selected page will be displayed here.'
        template = 'core/page_feature_block_snippet.html'

    def get_context(self, value, parent_context = None):
        context = super(PageFeatureBlock, self).get_context(value)
        try:
            if type(value.specific.body) == blocks.StreamValue:
                context['body_is_streamfield'] = True
        except AttributeError:
            pass  # If the page has no body, it's still valid
        return context


class ExpandableListItemBodyBlock(blocks.StreamBlock):
    rich_text = blocks.RichTextBlock()
    read_more = ReadMoreTagBlock()
    document_list = DocumentListBlock()


class ExpandableListItemBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    image = ImageChooserBlock()
    body = ExpandableListItemBodyBlock()

    class Meta:
        template = 'core/expandable_list_item_block_snippet.html'


class AutoIndexBlock(blocks.StaticBlock):
    class Meta:
        template = 'core/auto_index_block_snippet.html'


class IndexBlock(blocks.StructBlock):
    page = blocks.PageChooserBlock()

    class Meta:
        template = 'core/selectable_index_block_snippet.html'


class BadgeBlock(blocks.StructBlock):
    image = ImageChooserBlock()
    link = blocks.URLBlock()
    link_text = blocks.CharBlock()

    class Meta:
        template = 'core/badge_block.html'


class BadgeAreaBlock(blocks.ListBlock):
    class Meta:
        template = 'core/badge_area_block.html'


class AnchorBlock(blocks.StructBlock):
    name = blocks.CharBlock()

    class Meta:
        template = 'core/anchor_block.html'


class UpcomingServiceBlock(blocks.StaticBlock):
    class Meta:
        template = 'core/upcoming_service_block.html'

    def get_context(self, *args, **kwargs):
        context = super(UpcomingServiceBlock, self).get_context(*args, **kwargs)
        next_oos = (
            OrderOfService.objects.filter(date__gte=timezone.now())
            .order_by('date')
            .first()
        )
        if next_oos:
            context['next_service'] = next_oos.service.specific
            context['next_oos'] = next_oos
        return context


class UpcomingOrderOfServiceBlock(blocks.StaticBlock):
    class Meta:
        template = 'core/upcoming_oos_block.html'

    def get_context(self, *args, **kwargs):
        context = super(UpcomingOrderOfServiceBlock, self).get_context(*args, **kwargs)
        next_oos = (
            OrderOfService.objects.filter(date__gte=timezone.now())
            .order_by('date')
            .first()
        )
        if next_oos:
            context['next_service'] = next_oos.service.specific
            context['next_oos'] = next_oos
        return context


class ColumnBlock(blocks.StreamBlock):
    rich_text = blocks.RichTextBlock()


class MultiColumnBlock(blocks.StreamBlock):
    column = ColumnBlock(max_num=3)


class StepBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    body = blocks.RichTextBlock()
    image = ImageChooserBlock(required=False, help_text='Image associated with step in directions')


class DirectionsBlock(blocks.StreamBlock):
    step = StepBlock()

    class Meta:
        template = 'core/directions_block.html'


class SearchableTreeIndexBlock (blocks.StructBlock):
    page = blocks.PageChooserBlock()

    class Meta:
        template = 'core/searchable_tree_index_block.html'


class AdvancedFormBlock(SnippetChooserBlock):
    class Meta:
        template = 'core/advanced_form_block.html'


class CardBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    body = blocks.RichTextBlock()
    image = ImageChooserBlock()
    action_text = blocks.CharBlock()
    action_link = blocks.CharBlock()

    class Meta:
        template = 'core/card_block.html'


class CardContainerBlock(blocks.StreamBlock):
    card = CardBlock()


class BaseSectionBlock(blocks.StructBlock):
    heading = blocks.CharBlock()

    body_blocks = [
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
    ]


class SubSubSectionBlock(BaseSectionBlock):
    body = blocks.StreamBlock(
        BaseSectionBlock.body_blocks,
        required=False,
    )

    class Meta:
        template = 'core/section_block/subsubsection_block.html'


class SubSectionBlock(BaseSectionBlock):
    body = blocks.StreamBlock(
        BaseSectionBlock.body_blocks + [
            ('sub_sub_section', SubSubSectionBlock())
        ],
        required=False,
    )

    class Meta:
        template = 'core/section_block/subsection_block.html'


class SectionBlock(BaseSectionBlock):
    body = blocks.StreamBlock(
        BaseSectionBlock.body_blocks + [
            ('sub_section', SubSectionBlock())
        ],
        required=False,
    )

    class Meta:
        template = 'core/section_block/section_block.html'


class TableOfContentsBlock(blocks.StaticBlock):
    class Meta:
        icon = 'table'
        label = 'Show Table Of Contents'
        admin_text = f'{label}: This block generates a clickable table of contents, listing all Section blocks on the page.'
        template = 'core/table_of_contents_block.html'
