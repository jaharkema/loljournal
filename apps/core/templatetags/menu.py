from django import template
from django.core.urlresolvers import reverse

register = template.Library()


@register.simple_tag(takes_context=True)
def class_for_url(context, url):
    if '/' not in url:
        url = reverse(url)

    request = context['request']

    if request.get_full_path() == url:
        return 'active'

    return ''
