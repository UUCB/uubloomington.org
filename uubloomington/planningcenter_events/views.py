from django.http.response import HttpResponse
from .planningcenter_extras import get_events, update_events


# Create your views here.
def update_events_view(request):
    events = get_events()
    update_events(events)
    print(events)
    return HttpResponse("Update Events OK")
