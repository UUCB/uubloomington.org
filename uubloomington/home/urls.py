from django.urls import path

from home import views

urlpatterns = [
    path('next_carousel_image/<int:current_image_pk>',
         views.next_carousel_image,
         kwargs={'mode': 'forward'},
         name='next-carousel-image'
         ),
    path('previous_carousel_image/<int:current_image_pk>',
         views.next_carousel_image,
         kwargs={'mode': 'reverse'},
         name='previous-carousel-image'
         ),
    path('refresh_events/<int:page_pk>',
         views.refresh_events,
         name='refresh_events',
         ),
]