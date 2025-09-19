from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def get_site_config():
    """Return site configuration"""
    return settings.SITE_CONFIG


@register.simple_tag
def get_analytics_id():
    """Return Google Analytics ID"""
    return settings.GOOGLE_ANALYTICS_ID


@register.simple_tag
def get_plausible_domain():
    """Return Plausible domain"""
    return settings.PLAUSIBLE_DOMAIN