from wagtail import blocks
from django.utils.text import slugify


class GenericFieldBlock(blocks.StructBlock):
    label_text = blocks.CharBlock()
    placeholder_text = blocks.CharBlock(required=False)
    name_slug = blocks.CharBlock(required=False)
    required = blocks.BooleanBlock(required=False, default=False)

    def get_name_slug(self):
        if self.name_slug is not None:
            return self.name_slug
        else:
            return slugify(self.label_text)

    class Meta:
        template = 'advanced_forms/blocks/generic_field.html'


class SingleLineTextBlock(GenericFieldBlock):
    pass


class MultiLineTextBlock(GenericFieldBlock):
    class Meta:
        template = 'advanced_forms/blocks/multiline_text.html'


class TelephoneInputBlock(GenericFieldBlock):
    class Meta:
        template = 'advanced_forms/blocks/tel_field.html'


class EmailInputBlock(GenericFieldBlock):
    class Meta:
        template = 'advanced_forms/blocks/email_field.html'


class CheckboxesBlock(blocks.StructBlock):
    label_text = blocks.CharBlock()
    name_slug = blocks.CharBlock(required=False)
    options = blocks.ListBlock(blocks.CharBlock())

    class Meta:
        template = 'advanced_forms/blocks/checkboxes_block.html'


class RadioButtonsBlock(blocks.StructBlock):
    label_text = blocks.CharBlock()
    name_slug = blocks.CharBlock(required=False)
    options = blocks.ListBlock(blocks.CharBlock())

    class Meta:
        template = 'advanced_forms/blocks/radio_buttons_block.html'


class DropdownBlock(blocks.StructBlock):
    label_text = blocks.CharBlock()
    name_slug = blocks.CharBlock(required=False)
    options = blocks.ListBlock(blocks.CharBlock())

    class Meta:
        template = 'advanced_forms/blocks/dropdown_block.html'


class SubmitterEmailBlock(blocks.StructBlock):
    label_text = blocks.CharBlock(default='Your Email Address')
    placeholder_text = blocks.CharBlock(required=False, default='you@example.com')

    class Meta:
        template = 'advanced_forms/blocks/submitter_email.html'


class SubmitterNameBlock(blocks.StructBlock):
    label_text = blocks.CharBlock(default='Your Name')
    placeholder_text = blocks.CharBlock(required=False)

    class Meta:
        template = 'advanced_forms/blocks/submitter_name.html'


class RepeatingFormBlock(blocks.StreamBlock):
    single_line_text_field = SingleLineTextBlock()
    telephone_input_field = TelephoneInputBlock()
    email_input_field = EmailInputBlock()
    rich_text = blocks.RichTextBlock()
    checkboxes_field = CheckboxesBlock()
    radio_buttons_field = RadioButtonsBlock()
    dropdown_field = DropdownBlock()
    multi_line_text_field = MultiLineTextBlock()

    class Meta:
        template = 'advanced_forms/blocks/repeating_form.html'


class RepeatingFormContainerBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    fields = RepeatingFormBlock()

    class Meta:
        template = 'advanced_forms/blocks/repeating_form.html'
