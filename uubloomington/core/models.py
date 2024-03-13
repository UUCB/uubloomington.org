import django.forms
from django.core.mail import EmailMessage
from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, PageChooserPanel
from wagtail import blocks
from wagtail.embeds.blocks import EmbedBlock
from .blocks import ReadMoreTagBlock, ShowFeaturedImageBlock, PageFeatureBlock, ExpandableListItemBlock, AutoIndexBlock, IndexBlock, DocumentListBlock, BadgeAreaBlock, BadgeBlock, AnchorBlock, UpcomingServiceBlock, MultiColumnBlock, UpcomingOrderOfServiceBlock, DirectionsBlock
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import (
    FieldPanel, FieldRowPanel,
    InlinePanel, MultiFieldPanel
)
from wagtail.fields import RichTextField
from wagtail.contrib.forms.forms import FormBuilder
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField, FORM_FIELD_CHOICES
from wagtail.contrib.forms.panels import FormSubmissionsPanel
from core.widgets import TelephoneInput
from wagtail.admin.mail import send_mail


class Post(Page):
    body = RichTextField()
    featured_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    publish_in_newsletter = models.ForeignKey(
        "newsletter.Newsletter",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )

    intended_publication = models.DateField()

    content_panels = Page.content_panels + [
        FieldPanel('featured_image'),
        FieldPanel('body'),
        PageChooserPanel('publish_in_newsletter', page_type='newsletter.Newsletter'),
        FieldPanel('intended_publication'),
    ]


class PageWithPosts(Page):
    body = RichTextField()
    featured_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    show_posts = models.BooleanField(default=True)

    content_panels = Page.content_panels + [
        FieldPanel('featured_image'),
        FieldPanel('body'),
        FieldPanel('show_posts'),
    ]

    subpage_types = ['core.Post']


class GenericIndexPage(Page):
    body = RichTextField()
    featured_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    content_panels = Page.content_panels + [
        FieldPanel('featured_image'),
        FieldPanel('body'),
    ]


class StandardBlockPage(Page):
    featured_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    body = StreamField([
        ('rich_text', blocks.RichTextBlock()),
        ('read_more', ReadMoreTagBlock()),
        ('show_featured_image', ShowFeaturedImageBlock()),
        ('page_feature', PageFeatureBlock()),
        ('expandable_list', blocks.ListBlock(ExpandableListItemBlock)),
        ('embed', EmbedBlock(max_height=900)),
        ('auto_index', AutoIndexBlock()),
        ('selectable_index', IndexBlock()),
        ('document_list', DocumentListBlock()),
        ('badge_area', BadgeAreaBlock(child_block=BadgeBlock())),
        ('anchor', AnchorBlock()),
        ('upcoming_service', UpcomingServiceBlock()),
        ('upcoming_oos', UpcomingOrderOfServiceBlock()),
        ('multi_column', MultiColumnBlock()),
        ('directions', DirectionsBlock()),
    ], use_json_field=True, null=True)

    body_is_streamfield = True

    content_panels = Page.content_panels + [
        FieldPanel('featured_image'),
        FieldPanel('body'),
    ]

    def get_blocks_before_read_more(self):
        blocks_before_read_more = []
        found_read_more = False
        for block in self.body:
            if block.block_type != "read_more":
                blocks_before_read_more.append(block)
            else:
                found_read_more = True
                break
        if not found_read_more:
            blocks_before_read_more = [self.body[0]]
        return blocks_before_read_more


class FormField(AbstractFormField):
    CHOICES = FORM_FIELD_CHOICES + (
        ('tel', 'Telephone Number'),
    )
    page = ParentalKey('FormPage', on_delete=models.CASCADE, related_name='form_fields')
    field_type = models.CharField(
        verbose_name='field type',
        max_length=16,
        choices=CHOICES,
    )


class CustomFormBuilder(FormBuilder):
    def create_tel_field(self, field, options):
        return django.forms.CharField(widget=TelephoneInput, **options)


class FormPage(AbstractEmailForm):
    form_builder = CustomFormBuilder
    intro = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)
    send_confirmation_email = models.BooleanField(
        default=False,
        help_text="""
        If checked, this form will send a confirmation to the submitter.
        For this to work, your form MUST contain required fields for the submitter's name and email,
        and those fields must be specified below. 
        """
    )
    confirmation_email_greeting = models.TextField(
        blank=True,
        null=True,
        help_text="""
        Text to place at the beginning of the confirmation email, before the submitted data
        """
    )
    confirmation_email_ending = models.TextField(
        blank=True,
        null=True,
        help_text="""
        Text to place at the end of the confirmation email, after the submitted data
        """
    )
    name_field_name = models.CharField(
        blank=True,
        null=True,
        max_length=30,
        default='name',
        help_text="""
        The name of the field representing "name" for email purposes (usually where the submitter enters their name)
        """
    )
    email_field_name = models.CharField(
        blank=True,
        null=True,
        max_length=30,
        default='email',
        help_text="""
        The name of the field representing the submitter's email address
        """
    )
    featured_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    content_panels = AbstractEmailForm.content_panels + [
        FormSubmissionsPanel(),
        FieldPanel('featured_image'),
        FieldPanel('intro'),
        InlinePanel('form_fields', label="Form fields"),
        FieldPanel('thank_you_text'),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject'),
        ], "Email"),
        MultiFieldPanel(
            [
                FieldPanel('send_confirmation_email'),
                FieldPanel('confirmation_email_greeting'),
                FieldPanel('confirmation_email_ending'),
                FieldPanel('name_field_name'),
                FieldPanel('email_field_name'),
            ],
            "Confirmation Email Settings",
        )
    ]

    def send_mail(self, form):
        submitter_email = form.cleaned_data.get(self.email_field_name)
        submitter_name = form.cleaned_data.get(self.name_field_name)
        subject = self.subject
        if submitter_name:
            subject += f' from {submitter_name}'
        addresses = [address.strip() for address in self.to_address.split(",")]
        submission_email = EmailMessage(
            subject=subject,
            body=self.render_email(form),
            from_email=self.from_address,
            to=addresses,
            reply_to=[form.cleaned_data.get(self.email_field_name)]
        )
        submission_email.send()
        if self.send_confirmation_email and submitter_email:
            confirmation_email_text = f'{form.cleaned_data.get(self.name_field_name)},\n{self.confirmation_email_greeting}\n{self.render_email(form)}\n{self.confirmation_email_ending}'
            confirmation_email = EmailMessage(
                subject=self.subject,
                body=confirmation_email_text,
                from_email=self.from_address,
                to=(form.cleaned_data.get(self.email_field_name), ),
            )
            confirmation_email.send()

