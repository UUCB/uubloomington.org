from wagtail import blocks


class OOSGenericStreamBlock(blocks.StreamBlock):
    body = blocks.RichTextBlock()


class OOSElementBlock(blocks.StructBlock):
    header = blocks.CharBlock(required=False)
    info = blocks.RichTextBlock(required=False)

    class Meta:
        template = 'services/blocks/oos_element.html'


class OOSMultiColumnBlock(blocks.StreamBlock):
    column = OOSGenericStreamBlock()