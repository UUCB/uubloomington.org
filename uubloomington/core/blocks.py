from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.fields import StreamField
from wagtail.models import Page


class ReadMoreTagBlock(blocks.StaticBlock):
    class Meta:
        icon = 'arrow-down'
        label = '"Read More" tag'
        admin_text = f'{label}: Anything after this tag will be hidden behind a "Read More" button.'
        template = 'core/read_more_snippet.html'


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
        print(f'fieldtype {type(value.specific.body)}')
        if type(value.specific.body) == blocks.StreamValue:
            context['body_is_streamfield'] = True
        return context


class ExpandableListItemBodyBlock(blocks.StreamBlock):
    rich_text = blocks.RichTextBlock()
    read_more = ReadMoreTagBlock()


class ExpandableListItemBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    image = ImageChooserBlock()
    body = ExpandableListItemBodyBlock()

    class Meta:
        template = 'core/expandable_list_item_block_snippet.html'


class AutoIndexBlock(blocks.StaticBlock):
    class Meta:
        template = 'core/auto_index_block_snippet.html'

    def check_for_streamfield(self, page):
        if type(page.specific.body) == blocks.StreamValue:
            return True
        else:
            return False

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context)
        context['child_pages'] = [
            {'value': child_page, 'body_is_streamfield': self.check_for_streamfield(child_page)}
            for child_page
            in context['page'].get_children().live()
        ]
        return(context)
