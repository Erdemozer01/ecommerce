from django.template import Library
from article.models import Category, Posts

register = Library()


@register.simple_tag
def article_category_list():
    return Category.objects.all()


@register.filter(name='category_count')
def category_count(title):
    return Posts.objects.filter(category__title=title).count()


@register.simple_tag
def article_category_first():
    return Category.objects.all()[0:9]


@register.simple_tag
def article_category_second():
    return Category.objects.all()[9:18]


@register.simple_tag
def article_category_last():
    return Category.objects.all()[18:27]
