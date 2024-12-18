from django import template
from settings.models import SiteSettingMeta

register = template.Library()


@register.simple_tag
def meta_neumorphism():
    return SiteSettingMeta.objects.filter(meta__is_active=True, meta__name__icontains='neumorphism')
