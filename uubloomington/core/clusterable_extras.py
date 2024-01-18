from modelcluster.models import ClusterableModel
from django.db import models
from django.utils.translation import gettext_lazy as _

from wagtail.contrib.forms.models import FORM_FIELD_CHOICES
from wagtail.admin.panels import FieldPanel
from wagtail.api import APIField
from wagtail.contrib.forms.utils import get_field_clean_name


class ClusterableOrderable(ClusterableModel):
    sort_order = models.IntegerField(null=True, blank=True, editable=False)
    sort_order_field = "sort_order"

    class Meta:
        abstract = True
        ordering = ["sort_order"]


class ClusterableAbstractFormField(ClusterableOrderable):
    """
    Database Fields required for building a Django Form field.
    """

    clean_name = models.CharField(
        verbose_name=_("name"),
        max_length=255,
        blank=True,
        default="",
        help_text=_(
            "Safe name of the form field, the label converted to ascii_snake_case"
        ),
    )
    label = models.CharField(
        verbose_name=_("label"),
        max_length=255,
        help_text=_("The label of the form field"),
    )
    field_type = models.CharField(
        verbose_name=_("field type"), max_length=16, choices=FORM_FIELD_CHOICES
    )
    required = models.BooleanField(verbose_name=_("required"), default=True)
    choices = models.TextField(
        verbose_name=_("choices"),
        blank=True,
        help_text=_(
            "Comma or new line separated list of choices. Only applicable in checkboxes, radio and dropdown."
        ),
    )
    default_value = models.TextField(
        verbose_name=_("default value"),
        blank=True,
        help_text=_(
            "Default value. Comma or new line separated values supported for checkboxes."
        ),
    )
    help_text = models.CharField(
        verbose_name=_("help text"), max_length=255, blank=True
    )

    panels = [
        FieldPanel("label"),
        FieldPanel("help_text"),
        FieldPanel("required"),
        FieldPanel("field_type", classname="formbuilder-type"),
        FieldPanel("choices", classname="formbuilder-choices"),
        FieldPanel("default_value", classname="formbuilder-default"),
    ]

    api_fields = [
        APIField("clean_name"),
        APIField("label"),
        APIField("field_type"),
        APIField("help_text"),
        APIField("required"),
        APIField("choices"),
        APIField("default_value"),
    ]

    def get_field_clean_name(self):
        """
        Prepare an ascii safe lower_snake_case variant of the field name to use as the field key.
        This key is used to reference the field responses in the JSON store and as the field name in forms.
        Called for new field creation, validation of duplicate labels and form previews.
        When called, does not have access to the Page, nor its own id as the record is not yet created.
        """

        return get_field_clean_name(self.label)

    def save(self, *args, **kwargs):
        """
        When new fields are created, generate a template safe ascii name to use as the
        JSON storage reference for this field. Previously created fields will be updated
        to use the legacy unidecode method via checks & _migrate_legacy_clean_name.
        We do not want to update the clean name on any subsequent changes to the label
        as this would invalidate any previously submitted data.
        """

        is_new = self.pk is None
        if is_new:
            clean_name = self.get_field_clean_name()
            self.clean_name = clean_name

        super().save(*args, **kwargs)

    class Meta:
        abstract = True
        ordering = ["sort_order"]
