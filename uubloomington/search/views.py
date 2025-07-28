from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.template.response import TemplateResponse

from wagtail.models import Page
from wagtail.contrib.search_promotions.models import Query

from services.models import ServicePage, OrderOfService
from .utils import fuzzy_parse_query_string

from newsletter.models import Article, Newsletter, Issue


def search(request):
    search_query = request.GET.get("query", None)
    page = request.GET.get("page", 1)
    pages = Page.objects.live()

    # Search
    if search_query:
        # search_results = Page.objects.live().search(search_query)
        # query = Query.get(search_query)
        filters, query = fuzzy_parse_query_string(search_query)
        print(query)
        # Add filters here, pages=pages.filter(...)
        newsletter = filters.get('newsletter')
        if newsletter in ['yes', 'true']:
            pages = pages.exact_type(Article, Issue, Newsletter)
        if newsletter in ['no', 'false']:
            pages = pages.not_exact_type(Article, Issue, Newsletter)
        services = filters.get('services')
        if services in ['yes', 'true']:
            pages = pages.exact_type(ServicePage, OrderOfService)
        if services in ['no', 'false']:
            pages = pages.not_exact_type(ServicePage, OrderOfService)
        search_results = pages.search(query)

        # Record hit
        Query.get(search_query).add_hit()
    else:
        search_results = Page.objects.none()

    # Pagination
    paginator = Paginator(search_results, 10)
    try:
        search_results = paginator.page(page)
    except PageNotAnInteger:
        search_results = paginator.page(1)
    except EmptyPage:
        search_results = paginator.page(paginator.num_pages)

    return TemplateResponse(
        request,
        "search/search.html",
        {
            "search_query": search_query,
            "search_results": search_results,
        },
    )
