from django import template

register = template.Library()


@register.inclusion_tag('core/tags/pagination.html', takes_context=True)
def paginator(context):
    return context
