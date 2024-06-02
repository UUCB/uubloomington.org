from django.urls import path
from .views import *

urlpatterns = [
    path('process/', AdvancedFormResponseView.as_view(), name='process_advanced_form_response'),
]