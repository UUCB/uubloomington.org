from django.core.mail import EmailMessage
from django.db import models
from django.utils import timezone
from wagtail.fields import StreamField
from wagtail import blocks
import advanced_forms.blocks as advanced_forms_blocks
import json

from django.utils.text import slugify

FORM_FIELD_BLOCKS = [
    ('single_line_text_field', advanced_forms_blocks.SingleLineTextBlock()),
    ('telephone_input_field', advanced_forms_blocks.TelephoneInputBlock()),
    ('email_input_field', advanced_forms_blocks.EmailInputBlock()),
    ('checkboxes_field', advanced_forms_blocks.CheckboxesBlock()),
    ('radio_buttons_field', advanced_forms_blocks.RadioButtonsBlock()),
    ('dropdown_field', advanced_forms_blocks.DropdownBlock()),
    ('multi_line_text_field', advanced_forms_blocks.MultiLineTextBlock()),
]


def extract_field_slug(block):
    if block.value['name_slug']:
        return block.value['name_slug']
    else:
        return slugify(block.value['label_text'])


class AdvancedForm(models.Model):
    name = models.CharField(max_length=255)
    send_confirmation = models.BooleanField(default=False)
    notification_email = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text='Enter email addresses to notify of submissions to this form, separated by commas.'
    )
    form_fields = StreamField(
        FORM_FIELD_BLOCKS + [
            ('rich_text', blocks.RichTextBlock()),
            ('repeating_fields', advanced_forms_blocks.RepeatingFormContainerBlock()),
            ('submitter_name_field', advanced_forms_blocks.SubmitterNameBlock()),
            ('submitter_email_field', advanced_forms_blocks.SubmitterEmailBlock()),
        ],
        block_counts = {
            'submitter_name_field': {'min_num': 1, 'max_num': 1},
            'submitter_email_field': {'min_num': 1, 'max_num': 1},
            'repeating_fields': {'max_num': 1},
        }
    )
    confirmation_text = models.TextField(null=True, blank=True)

    def get_current_field_names(self):
        name_slugs = []
        for block in self.form_fields:
            if block.block_type in dict(FORM_FIELD_BLOCKS).keys():
                name_slugs.append(extract_field_slug(block))
            if block.block_type == 'repeating_fields':
                pass
                for block in block.value['fields']:
                    if block.block_type in dict(FORM_FIELD_BLOCKS).keys():
                        name_slugs.append(extract_field_slug(block))
        return name_slugs

    def get_current_field_labels(self):
        labels = []
        for block in self.form_fields:
            if block.block_type in dict(FORM_FIELD_BLOCKS).keys():
                labels.append(block.value['label_text'])
            if block.block_type == 'repeating_fields':
                for block in block.value['fields']:
                    if block.block_type in dict(FORM_FIELD_BLOCKS).keys():
                        labels.append(block.value['label_text'])
        return labels

    def __str__(self):
        return self.name


class AdvancedFormResponse(models.Model):
    submitter_name = models.CharField(max_length=500)
    submitter_email = models.EmailField()
    response_json = models.JSONField()
    submission_datetime = models.DateTimeField(default=timezone.now)
    form = models.ForeignKey(AdvancedForm, on_delete=models.CASCADE, related_name='responses')

    def get_current_values(self):
        keys = self.form.get_current_field_names()
        values = []
        for key in keys:
            values.append((key, json.loads(self.response_json).get(key)))
        return values

    def __str__(self):
        return f'Response from {self.submitter_name}'
