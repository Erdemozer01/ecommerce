from django import template
from settings.models import SiteSettingModels

register = template.Library()


@register.simple_tag
def neuromorphism_general_settings():
    try:
        site = SiteSettingModels.objects.filter(is_active=True)
        if site.get(theme__icontains='neumorphism'):
            site = site.get(theme__icontains='neumorphism')
            return site
    except:
        return None