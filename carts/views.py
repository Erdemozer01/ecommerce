from django.views import generic
from django.shortcuts import redirect, reverse, get_object_or_404
from django.http import HttpResponseRedirect
from store.models import Product
from .models import Cart, CartItems
from django.conf import settings
from django.contrib import messages
from django.db.models import Sum
from django.contrib.auth.models import User


class FavoriteListView(generic.ListView):
    template_name = 'pages/favorite.html'
    model = Product

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['cart_items'] = CartItems.objects.filter(cart__customer=self.request.user.pk)
            total = CartItems.objects.filter(cart__customer=self.request.user.pk).aggregate(Sum('total'))
            context['total'] = total.get('total__sum')
            context['my_favorites'] = Product.objects.filter(likes=self.request.user)

        return context


class CartListView(generic.ListView):
    template_name = 'pages/cart.html'
    model = CartItems
    context_object_name = 'cart_items'

    def get_queryset(self):
        return CartItems.objects.filter(cart__customer=self.request.user.pk)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            total = CartItems.objects.filter(cart__customer=self.request.user.pk).aggregate(Sum('total'))
            context['my_favorites'] = Product.objects.filter(likes=self.request.user)
            context['total'] = total.get('total__sum')
        return context


def add_cart(request, user, product_code):
    if request.user.is_anonymous:
        messages.error(request, "Lütfen Giriş Yapınız")
        return redirect('%s?next=/magaza/products/' % (settings.LOGIN_URL))
    product = Product.objects.get(product_code=product_code)
    try:
        cart = Cart.objects.get(customer=request.user)
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            customer=request.user,
        )

    cart.save()

    try:
        cart_item = CartItems.objects.get(product=product, cart=cart)
        cart_item.quantity += 1
        cart_item.total = cart_item.quantity * cart_item.product.price
        cart_item.save()

    except CartItems.DoesNotExist:
        cart_item = CartItems.objects.create(
            product=product,
            quantity=1,
            cart=cart
        )
        cart_item.total = cart_item.quantity * cart_item.product.price
        cart_item.save()
    return HttpResponseRedirect(reverse('carts:sepetim', kwargs={'user': request.user}))


def add_favorite(request, slug):
    global product
    if request.user.is_anonymous:
        messages.error(request, "Favorilere eklemek için giriş yapınız")
        return redirect('%s?next=/magaza/products/' % (settings.LOGIN_URL))

    product = Product.objects.get(slug=slug)
    product.likes.add(request.user)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def delete_item_cart(request, user_id, product_code):
    if request.user.is_anonymous:
        messages.error(request, "Favorilere eklemek için giriş yapınız")
        return redirect('%s?next=/magaza/products/' % (settings.LOGIN_URL))
    product = CartItems.objects.get(product__product_code=product_code, cart__customer=user_id)
    product.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def delete_item_favorite(request, slug):
    if request.user.is_anonymous:
        messages.error(request, "Favorilere eklemek için giriş yapınız")
        return redirect('%s?next=/magaza/products/' % (settings.LOGIN_URL))
    product = Product.objects.get(slug=slug)
    product.likes.remove(request.user)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
