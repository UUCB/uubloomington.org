import json

from django.forms import ModelForm, ValidationError

from advanced_forms.models import AdvancedFormResponse, extract_field_slug, FORM_FIELD_BLOCKS


class AdvancedFormResponseForm(ModelForm):
    def clean(self):
        cleaned_data = super(AdvancedFormResponseForm, self).clean()
        # TODO: Validate that the JSON doesn't include any fields which aren't specified in the form
        advanced_form_instance = cleaned_data['form']
        response = self.cleaned_data.get('response_json')
        flattened_response = []
        # Construct a flat list of all form field responses, even repeated ones.
        # Here, we derive the order and field names from StreamField blocks representing the form, rather than the
        # contents of the submission.
        for block in advanced_form_instance.form_fields:
            if block.block_type in dict(FORM_FIELD_BLOCKS).keys():
                try:  # Try to append the field name and value.
                    flattened_response.append({
                        'field_name': extract_field_slug(block),
                        'value': response.get('constantValues')[extract_field_slug(block)],
                    })
                except KeyError:  # KeyError means the field wasn't present in the HTTP request. Assume it is "None".
                                  # This will be the case for certain field types (checkboxes and radio buttons)
                                  # which do not appear in the form as JSON when nothing is selected.
                    flattened_response.append({
                        'field_name': extract_field_slug(block),
                        'value': None,
                    })
            elif block.block_type == 'repeating_fields':  # When we get to a repeating fields block in the source
                                                          # document, pause and repeat the above process once for each
                                                          # repeat present in the received submission.
                for repeat in response.get('repeatedValues'):
                    for field in block.value['fields']:
                        if field.block_type in dict(FORM_FIELD_BLOCKS).keys():
                            try:  # Try to append the field name and value.
                                flattened_response.append({
                                    'field_name': extract_field_slug(field),
                                    'value': repeat[extract_field_slug(field)],
                                })
                            except KeyError:  # KeyError is possible here; explained above.
                                flattened_response.append({
                                    'field_name': extract_field_slug(field),
                                    'value': None,
                                })
        # Now, let's validate that all required fields contain *something*.
        required_fields = advanced_form_instance.get_required_fields()
        missing_required_fields_by_sequence = []
        # The sequence referenced here is the order that the form fields appear on the page, not including
        # submitter email and name fields (handled as separate form fields). This sequence does include repeating
        # fields, *as many times as they exist in the submission* so that we can accurately point to which repeating
        # field is missing a value.
        #
        # By flattening the submission this way, we gain the use of this much simpler method of validating each field on
        # its own (currently just required fields, but this should be easily expandable). Plus, this aligns better with
        # easy-to-implement ways of identifying fields in _hyperscript on the frontend. By passing a simple list of
        # field sequence numbers which are problematic, we can very simply highlight those fields, even though the
        # Django forms backend doesn't know our field names.
        for index, field in enumerate(flattened_response, start=1):
            # TODO: Duplicate field name slugs could cause misidentified required fields. Fix this eventually.
            if field['field_name'] in required_fields and not field['value']:
                missing_required_fields_by_sequence.append(index)
        if missing_required_fields_by_sequence:
            raise ValidationError(message=missing_required_fields_by_sequence)
        return cleaned_data

    class Meta:
        model = AdvancedFormResponse
        fields = [
            'submitter_name',
            'submitter_email',
            'response_json',
            'form',
        ]
