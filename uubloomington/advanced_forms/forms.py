import json

from django.forms import ModelForm, ValidationError

from advanced_forms.models import AdvancedFormResponse


class AdvancedFormResponseForm(ModelForm):
    def clean(self):
        cleaned_data = super(AdvancedFormResponseForm, self).clean()
        # TODO: Validate that the JSON doesn't include any fields which aren't specified in the form
        advanced_form_instance = cleaned_data['form']
        required_fields = advanced_form_instance.get_required_fields()
        response = self.cleaned_data.get('response_json')
        flattened_response = [
            {'field_name': 'submitter_name', 'value': self.cleaned_data.get('submitter_name')},
            {'field_name': 'submitter_email', 'value': self.cleaned_data.get('submitter_email')},
        ] + [
            {'field_name': key, 'value': value} for key, value in response.get('constantValues').items()
        ] + [
            {'field_name': key, 'value': value} for repeat in response.get('repeatedValues') for key, value in repeat.items()
        ]
        print(flattened_response)
        missing_required_fields_by_sequence = []
        for index, field in enumerate(flattened_response, start=1):
            if field['field_name'] in required_fields and not field['value']:
                missing_required_fields_by_sequence.append(index)
        if missing_required_fields_by_sequence:
            print(missing_required_fields_by_sequence)
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
