from wagtail.api.v2.views import PagesAPIViewSet
from wagtail.api.v2.router import WagtailAPIRouter
from wagtail.images.api.v2.views import ImagesAPIViewSet
from wagtail.documents.api.v2.views import DocumentsAPIViewSet
from rest_framework.response import Response
from rest_framework import serializers

from services.models import ServicePage

# Create the router. "wagtailapi" is the URL namespace
api_router = WagtailAPIRouter('wagtailapi')

class ServicesShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServicePage

class ServicesAPIViewSet(PagesAPIViewSet):
    model = ServicePage

    def listing_view(self, request):
        available_services = ServicePage.objects.all().order_by('-order_of_service__date')
        output = {
            'meta': {
                "total_count": available_services.count(),
            },
            "items": [
                {
                    "id": service_page.pk,
                    "meta": {
                        "name": service_page.title,
                        "date": service_page.order_of_service.first().date,
                        "url": f"{request.build_absolute_uri()}{service_page.pk}/",
                    }
                }
                for service_page in available_services
            ]
        }
        return Response(output)

    def detail_view(self, request, *args, **kwargs):
        # implement some "get the OOS fields" nonsense here, pushing out some easy-to-parse JSON which will work for OpenShow
        service_page = self.get_object().specific
        program = service_page.order_of_service.first().program
        segments = [
            {
                "name": element.value['header'],
                "details": str(element.value['info']),
            }
            for element in program
            if element.block_type == 'element'
        ]
        show_dict = {
            'name': f'{service_page.order_of_service.first().date} -{service_page.title.split(":", maxsplit=1)[1]}',
            'description': service_page.body,
            'date': service_page.order_of_service.first().date,
            'id': service_page.pk,
            'segments': segments,
        }
        return Response(show_dict)



# Add the three endpoints using the "register_endpoint" method.
# The first parameter is the name of the endpoint (such as pages, images). This
# is used in the URL of the endpoint
# The second parameter is the endpoint class that handles the requests
api_router.register_endpoint('pages', PagesAPIViewSet)
api_router.register_endpoint('images', ImagesAPIViewSet)
api_router.register_endpoint('documents', DocumentsAPIViewSet)
api_router.register_endpoint('services', ServicesAPIViewSet)