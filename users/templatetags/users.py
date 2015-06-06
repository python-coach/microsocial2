from django import template
from django.conf import settings


register = template.Library()


@register.filter
def get_avatar(user):
    try:
        return user.avatar.url
    except ValueError:
        return '{}users/img/empty_avatar.png'.format(settings.STATIC_URL)
