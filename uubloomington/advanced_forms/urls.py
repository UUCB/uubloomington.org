from django.urls import path
from .views import *

urlpatterns = [
    path('process/', AdvancedFormResponseView.as_view(), name='process_advanced_form_response'),
    path('<int:pk>/export_xlsx', AdvancedFormResponseExportXlsxView.as_view(), name='export_advanced_form_response_xlsx'),
    path('<int:pk>/export_csv', AdvancedFormResponseExportCsvView.as_view(), name='export_advanced_form_response_csv'),
]
