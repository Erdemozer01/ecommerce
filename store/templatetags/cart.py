from django import template
from store.models import Cart, Product, CartItems

register = template.Library()


@register.simple_tag
def cart_items_count(user):
    return Cart.objects.filter(customer__username=user).count()


@register.filter(name='request', )
def wish_list_count(request, user):
    return Product.objects.filter(wish_list__username=user).count()
