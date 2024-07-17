from django.shortcuts import render
from django.views.generic import FormView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponseBadRequest, HttpResponse
from django.core.mail import EmailMessage
from wagtail.snippets.views.snippets import InspectView

from .forms import AdvancedFormResponseForm
from .models import AdvancedFormResponse, AdvancedForm

import json

import openpyxl
import tempfile


class AdvancedFormResponseView(FormView):
    form_class = AdvancedFormResponseForm
    extra_context = {}

    # Disable GET requests, the frontend of this form is generated elsewhere
    def get(self, request, *args, **kwargs):
        return HttpResponseBadRequest()

    def send_confirmation_email(self, form):
        message_text = f'{form.cleaned_data["submitter_name"]},\n\n{form.cleaned_data["form"].confirmation_text}'
        confirmation_email = EmailMessage(
            to=[form.cleaned_data['submitter_email'],],
            subject=f'Thank you for your submission to "{form.cleaned_data["form"].name}"!',
            body=message_text,
            from_email='noreply@website.uubloomington.org'
        )
        confirmation_email.send()

    def form_valid(self, form):
        print(form.cleaned_data)
        print('HELLO')
        dynamic_response = form.cleaned_data['response_json']
        repeated_values = dynamic_response.get('repeatedValues')
        constant_values = dynamic_response.get('constantValues')
        if repeated_values:
            for submission in repeated_values:
                response_out = constant_values.copy()
                response_out.update(submission)
                AdvancedFormResponse.objects.create(
                    response_json=json.dumps(response_out),
                    form=form.cleaned_data['form'],
                    submitter_name=form.cleaned_data['submitter_name'],
                    submitter_email=form.cleaned_data['submitter_email'],
                )
        else:
            AdvancedFormResponse.objects.create(
                response_json=json.dumps(form.cleaned_data['constant_values']),
                form=form.cleaned_data['form'],
                submitter_name=form.cleaned_data['submitter_name'],
                submitter_email=form.cleaned_data['submitter_email'],
            )
        self.template_name = 'advanced_forms/valid.html'
        if form.cleaned_data['form'].send_confirmation:
            self.send_confirmation_email(form)
        return self.render_to_response(self.get_context_data(form=form))

    def form_invalid(self, form):
        self.template_name = 'advanced_forms/invalid.html'
        self.extra_context['test'] = 'HI IMA TEST'
        self.extra_context['problematic_fields'] = list(form.errors.as_data().keys())
        return super(self.__class__, self).form_invalid(form)


class AdvancedFormInspectView(InspectView):
    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)
        context['']


class AdvancedFormResponseExportXlsxView(LoginRequiredMixin, DetailView):
    model = AdvancedForm

    login_url = '/admin/login'

    def get(self, request, *args, **kwargs):
        advanced_form_object = self.get_object()
        workbook = openpyxl.Workbook()
        worksheet = workbook.active
        # Insert the headers
        worksheet.append([key for key in advanced_form_object.get_current_field_labels()])
        # Make columns the right size, sort of
        for column in worksheet.columns:
            cell = column[0]
            if len(str(cell.value)) > 13:
                worksheet.column_dimensions[cell.column_letter].width = len(str(cell.value)) + 2
        # Insert the actual data
        for response in advanced_form_object.responses.all():
            worksheet.append([str(value[1]) for value in response.get_current_values()])
        response = HttpResponse(content_type='application/ms-excel')
        with tempfile.NamedTemporaryFile() as tmp:
            workbook.save(tmp)
            tmp.seek(0)
            response.write(tmp.read())
        return response
