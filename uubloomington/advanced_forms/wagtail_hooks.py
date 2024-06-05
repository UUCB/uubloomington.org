from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet
from wagtail.admin.panels import FieldPanel, TabbedInterface, ObjectList

from .models import AdvancedForm


class AdvancedFormViewset(SnippetViewSet):
    model = AdvancedForm

    panels = [
        FieldPanel('name'),
        FieldPanel('notification_email'),
        FieldPanel('form_fields'),
    ]

    confirmation_panels = [
        FieldPanel('send_confirmation'),
        FieldPanel('confirmation_text'),
    ]

    edit_handler = TabbedInterface([
        ObjectList(panels, heading='Form Fields'),
        ObjectList(confirmation_panels, heading='Confirmation'),
    ])

    inspect_view_enabled = True
    inspect_template_name = 'advanced_forms/inspect_advanced_form.html'

    add_to_admin_menu = True


register_snippet(AdvancedFormViewset)