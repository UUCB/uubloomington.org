from wagtail import blocks


class OOSGenericStreamBlock(blocks.StreamBlock):
    body = blocks.RichTextBlock()


class OOSParticipantStreamBlock(blocks.StreamBlock):
    # TODO: Add some dynamic content to orders of service, such as hover-over bios of people and groups
    # person = blocks.PageChooserBlock()
    text = blocks.TextBlock()


class OOSElementBlock(blocks.StructBlock):
    header = blocks.CharBlock(required=False)
    info = OOSParticipantStreamBlock(required=False)

    class Meta:
        template = 'services/blocks/oos_element.html'


class OOSMultiColumnBlock(blocks.StreamBlock):
    column = OOSGenericStreamBlock()