from django.urls import path
from planningcenter_events import views

urlpatterns = [
    path('update_events', views.update_events_view, name='update_events'),
]
