from django.forms.widgets import Input


class TelephoneInput(Input):
    input_type = 'tel'
    template_name = 'django/forms/widgets/text.html'