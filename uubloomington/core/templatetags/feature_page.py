from django import template
from wagtail import blocks

register = template.Library()


@register.inclusion_tag('core/page_feature_block_snippet.html')
def feature_page(page):
    context = {
        'value': page,
        'page': page,
    }
    if type(page.specific.body) == blocks.StreamValue:
        context['body_is_streamfield'] = True
    return context
