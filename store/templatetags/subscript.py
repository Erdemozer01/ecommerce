from django import template
from store.models import Product, NewsLetter
from article.models import Posts

register = template.Library()


@register.simple_tag
def subscript_product():
    return Product.objects.order_by("-created")[:10]


@register.simple_tag
def subscript_article():
    return Posts.objects.order_by("-created")[:3]



@register.simple_tag
def newsletter():
    return NewsLetter.objects.latest()