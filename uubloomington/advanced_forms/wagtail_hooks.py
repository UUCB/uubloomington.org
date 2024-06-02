from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet
from wagtail.admin.panels import FieldPanel

from .models import AdvancedForm


class AdvancedFormViewset(SnippetViewSet):
    model = AdvancedForm

    panels = [
        FieldPanel('name'),
        FieldPanel('send_confirmation'),
        FieldPanel('notification_email'),
        FieldPanel('form_fields'),
    ]

    inspect_view_enabled = True
    inspect_template_name = 'advanced_forms/inspect_advanced_form.html'

    add_to_admin_menu = True


register_snippet(AdvancedFormViewset)