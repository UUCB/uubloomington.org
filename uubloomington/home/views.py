from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.http import HttpResponse
from .models import HomePageCarouselImages
from wagtail.models import Page
from core import planningcenter_extras


def next_carousel_image(request, current_image_pk, mode):
    current_image = get_object_or_404(HomePageCarouselImages, pk=current_image_pk)
    potential_images = current_image.page.carousel_images.all()
    for index, image in enumerate(potential_images):
        if current_image == {
            'forward': current_image.page.carousel_images.last(),
            'reverse': current_image.page.carousel_images.first(),
        }[mode]:
            return render(request, 'home/carousel_image.html', {
                'carousel_image': {
                    'forward': potential_images[0],
                    'reverse': potential_images.last(),
                }[mode],
            })
        elif current_image == image:
            return render(request, 'home/carousel_image.html', {
                'carousel_image': potential_images[index +
                                                   {
                                                       'forward': 1,
                                                       'reverse': -1,
                                                   }[mode]
                                                   ],
            })


def refresh_events(request, page_pk):
    page = Page.objects.get(pk=page_pk).specific
    page.upcoming_events = planningcenter_extras.get_upcoming_events(page.display_next_events)
    page.upcoming_events_last_checked = timezone.now()
    page.save()
    return HttpResponse("Refresh Events OK")
