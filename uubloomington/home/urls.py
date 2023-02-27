from django.urls import path

from home import views

urlpatterns = [
    path('next_carousel_image/<int:current_image_pk>', views.next_carousel_image, name='next-carousel-image')
]