from django import template
from django.conf import settings

register = template.Library()


@register.inclusion_tag('core/tags/champion_icon.html', takes_context=True)
def icon_for_champion(context, name):
    icon_url = '{0}/{1}/img/champion/{2}.png'.format(
        settings.DDRAGON_CDN_URI,
        settings.DDRAGON_VERSION,
        name,
    )

    return {
        'icon_url': icon_url,
        'champion_name': name,
    }
