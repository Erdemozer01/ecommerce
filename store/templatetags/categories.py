from django import template
from store.models import ProductCategory, Product
from article.models import Category

register = template.Library()


@register.simple_tag()
def product_categories_list_for_sidebar_menu_first_level():
    return ProductCategory.objects.all()[:9]

@register.simple_tag()
def product_categories_list_for_sidebar_menu_second_level():
    return ProductCategory.objects.all()[9:18]

@register.simple_tag()
def product_categories_list_for_sidebar_menu_last_level():
    return ProductCategory.objects.all()[18:27]

@register.filter(name='product_cat_count')
def product_category_count(category):
    return Product.objects.filter(category__title=category).count()