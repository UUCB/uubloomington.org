from django.shortcuts import render, get_object_or_404
from .models import HomePageCarouselImages


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
