from wagtail import blocks


class OOSGenericStreamBlock(blocks.StreamBlock):
    body = blocks.RichTextBlock()


class OOSParticipantStreamBlock(blocks.StreamBlock):
    person = blocks.PageChooserBlock()
    text = blocks.TextBlock()


class OOSElementBlock(blocks.StructBlock):
    header = blocks.CharBlock(required=False)
    participants = OOSParticipantStreamBlock(required=False)
    body = blocks.RichTextBlock(required=False)

    class Meta:
        template = 'services/blocks/oos_element.html'


class OOSMultiColumnBlock(blocks.StructBlock):
    column = blocks.ListBlock(OOSGenericStreamBlock)