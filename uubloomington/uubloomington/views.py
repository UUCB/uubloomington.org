from django.core.management import call_command
from django.http import HttpResponse


def publish_scheduled(request):
    call_command('publish_scheduled')
    return HttpResponse('OK')


def reindex_search(request):
    call_command('update_index')
    return HttpResponse('OK')