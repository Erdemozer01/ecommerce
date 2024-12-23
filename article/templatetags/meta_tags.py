from django import template

register = template.Library()

@register.filter(name='rsplit_keywords')
def rsplit(value):
    return ",".join(str(x) for x in value.rsplit('-', ))