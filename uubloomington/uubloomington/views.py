from django.core.management import call_command
from django.http import HttpResponse


def publish_scheduled(request):
    call_command('publish_scheduled')
    return HttpResponse('OK')
