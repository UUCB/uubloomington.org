from django.shortcuts import render, get_object_or_404
from .models import HomePageCarouselImages


def next_carousel_image(request, current_image_pk):
    current_image = get_object_or_404(HomePageCarouselImages, pk=current_image_pk)
    potential_images = current_image.page.carousel_images.all()
    for index, image in enumerate(potential_images):
        if current_image == current_image.page.carousel_images.last():
            return render(request, 'home/carousel_image.html', {
                'carousel_image': potential_images[0],
            })
        elif current_image == image:
            return render(request, 'home/carousel_image.html', {
                'carousel_image': potential_images[index + 1],
            })

