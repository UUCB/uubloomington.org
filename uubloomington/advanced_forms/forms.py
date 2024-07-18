from django.forms import ModelForm

from advanced_forms.models import AdvancedFormResponse


class AdvancedFormResponseForm(ModelForm):
    def clean(self):
        cleaned_data = super(AdvancedFormResponseForm, self).clean()
        # TODO: Validate that the JSON doesn't include any fields which aren't specified in the form
        return cleaned_data

    class Meta:
        model = AdvancedFormResponse
        fields = '__all__'
