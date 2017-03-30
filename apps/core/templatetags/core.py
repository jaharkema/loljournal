from django import template
from django.http import QueryDict

register = template.Library()


@register.simple_tag(takes_context=True)
def add_param_to_get(context, key, value):
    request = context['request']

    # Change the QueryDict to a regular dict to make sure it does not contain
    # duplicate keys
    regular_dict = request.GET.dict()
    regular_dict.update({key: value})

    query_dict = QueryDict(mutable=True)
    query_dict.update(regular_dict)

    return '?' + query_dict.urlencode()
