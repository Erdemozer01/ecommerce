import decimal
import os
from datetime import datetime
from smtplib import SMTPAuthenticationError

from django.db.models.aggregates import Max
from django.template.loader import get_template

from settings.models import SiteSettingModels
from django.contrib import messages

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.conf import settings
from django.db.models import Sum, Count, Max

from accounts.models import Profile
from .models import Product, ProductComments, Cart, PromoCodeModel, CartItems, Subscribe, Alert
from django.db.models import Q
from hitcount.views import HitCountDetailView
from accounts.forms import CheckOutForm
from .forms import PromoCodeForm, ContactForm
from django.utils.timezone import now
from django.core.mail import send_mail, EmailMultiAlternatives


class ProductCategoryView(ListView):
    template_name = "pages/category_list.html"
    model = Product
    context_object_name = "product_category_list"
    paginate_by = 9

    def get_queryset(self):
        search = self.request.GET.get('search', False)
        if search:
            object_list = Product.objects.filter(Q(title__icontains=search) | Q(category__title__icontains=search) |
                                                 Q(brand__icontains=search))
            if object_list.exists():
                messages.add_message(self.request, messages.SUCCESS, f'{object_list.count()} Ürün Bulundu.')
                return object_list
            else:
                messages.add_message(self.request, messages.ERROR, 'Aradığınız Ürün Bulunamadı')
                return self.model.objects.all()
        else:
            return Product.objects.filter(category__title__icontains=self.kwargs['category'])

    def get_context_data(self, **kwargs):
        context = super(ProductCategoryView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            cart_id = self.request.session.session_key
            context['wish_list_products'] = Product.objects.filter(wish_list__username=self.request.user)
            context['cart_list'] = CartItems.objects.filter(cart__cart_id=cart_id).aggregate(Sum('quantity'))[
                'quantity__sum']

        context['cart_id'] = self.request.session.session_key
        context['category'] = self.kwargs['category']

        return context


class BrandCategoryView(ListView):
    template_name = "pages/category_list.html"
    model = Product
    context_object_name = "product_brand_list"
    paginate_by = 9

    def get_queryset(self):
        search = self.request.GET.get('search', False)
        if search:
            object_list = Product.objects.filter(Q(title__icontains=search) | Q(category__title__icontains=search) |
                                                 Q(brand__icontains=search))
            if object_list.exists():
                messages.add_message(self.request, messages.SUCCESS, f'{object_list.count()} Ürün Bulundu.')
                return object_list
            else:
                messages.add_message(self.request, messages.ERROR, 'Aradığınız Ürün Bulunamadı')
                return self.model.objects.all()
        else:
            return Product.objects.filter(brand__icontains=self.kwargs['brand'])

    def get_context_data(self, **kwargs):
        context = super(BrandCategoryView, self).get_context_data(**kwargs)
        # Navbar
        if self.request.user.is_authenticated:
            cart_id = self.request.session.session_key
            context['wish_list_products'] = Product.objects.filter(wish_list__username=self.request.user)
            context['cart_list'] = CartItems.objects.filter(cart__cart_id=cart_id).aggregate(Sum('quantity'))[
                'quantity__sum']
        context['brand'] = self.kwargs['brand']
        return context


class StoreListView(ListView):
    template_name = "pages/store_list.html"
    model = Product
    context_object_name = "product_list"
    paginate_by = 36

    def get(self, request, *args, **kwargs):
        try:
            for promo in PromoCodeModel.objects.all():
                if promo.promo_end_date < now():
                    promo.delete()
        except PromoCodeModel.DoesNotExist:
            pass
        return super(StoreListView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        search = self.request.GET.get('search', False)

        min_price = self.request.GET.get('en_dusuk', False)
        max_price = self.request.GET.get('en_yuksek', False)

        object_list = Product.objects.all()

        if search:

            object_list = object_list.filter(Q(title__icontains=search) | Q(category__title__icontains=search) | Q(
                brand__icontains=search))

            if object_list.exists():
                messages.add_message(self.request, messages.SUCCESS, f'{object_list.count()} Ürün Bulundu.')
            else:
                messages.add_message(self.request, messages.ERROR, 'Aradığınız Ürün Bulunamadı')
            return object_list

        if min_price or max_price:

            if not max_price:
                max_price = object_list.aggregate(Max('price'))['price__max']

            object_list = object_list.filter(Q(price__lte=float(max_price)) & Q(price__gte=float(min_price)))

        return object_list

    def get_context_data(self, **kwargs):
        context = super(StoreListView, self).get_context_data(**kwargs)
        cart_id = self.request.session.session_key
        # Navbar_wish_list
        if self.request.user.is_authenticated:
            context['wish_list_products'] = Product.objects.filter(wish_list__username=self.request.user)
            context['cart_list'] = CartItems.objects.filter(cart__cart_id=cart_id).aggregate(Sum('quantity'))[
                'quantity__sum']

        context['alert_list'] = Alert.objects.filter(is_publish=True)

        return context


class ProductDetailView(HitCountDetailView, DetailView):
    template_name = "pages/store_detail.html"
    model = Product
    context_object_name = "product"
    count_hit = True

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            cart_id = self.request.session.session_key
            context['wish_list_products'] = Product.objects.filter(wish_list__username=self.request.user)
            context['cart_list'] = CartItems.objects.filter(cart__cart_id=cart_id).aggregate(Sum('quantity'))[
                'quantity__sum']

        context['related_products'] = Product.objects.filter(category=self.object.category).exclude(id=self.object.id)[
                                      :3]
        context['comments'] = ProductComments.objects.filter(product_id=self.kwargs['pk'])

        return context

    def post(self, request, *args, **kwargs):

        product_obj = self.get_object()

        if self.get_object().product_comment.filter(user=self.request.user).exists():
            self.get_object().product_comment.filter(user=self.request.user).delete()
            comment = ProductComments.objects.create(product_id=product_obj.pk, user=request.user,
                                                     comment=request.POST['comment'])
            messages.add_message(request, messages.SUCCESS,
                                 'Daha önceden yorum yaptığınız için yorumunuz güncellenmiştir...')

            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        else:
            comment = ProductComments.objects.create(product_id=product_obj.pk, user=request.user,
                                                     comment=request.POST['comment'])
            messages.add_message(request, messages.SUCCESS, 'Yorumunuz başarılı şekilde eklenmiştir...')

            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class SortByLowPriceView(ListView):
    template_name = "pages/store_list.html"
    model = Product
    context_object_name = "product_list"
    paginate_by = 36

    def get_queryset(self):
        search = self.request.GET.get('search', False)
        object_list = Product.objects.order_by('price')
        if search:
            object_list = object_list.filter(Q(title__icontains=search) | Q(category__title__icontains=search) | Q(
                brand__icontains=search))
            if object_list.exists():
                if object_list.filter(is_discount=True).exists():
                    object_list = object_list.order_by('-discount_price')
                else:
                    object_list = object_list.order_by('price')
                messages.add_message(self.request, messages.SUCCESS, f'{object_list.count()} Ürün Bulundu.')
                return object_list
            else:
                messages.add_message(self.request, messages.ERROR, 'Aradığınız Ürün Bulunamadı')
                return object_list
        if object_list.filter(is_discount=True).exists():
            object_list = object_list.order_by('-discount_price')

        return object_list

    def get_context_data(self, **kwargs):
        context = super(SortByLowPriceView, self).get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            cart_id = self.request.session.session_key
            context['wish_list_products'] = Product.objects.filter(wish_list__username=self.request.user)
            context['cart_list'] = CartItems.objects.filter(cart__cart_id=cart_id).aggregate(Sum('quantity'))[
                'quantity__sum']

        return context


class SortByHighPriceView(ListView):
    template_name = "pages/store_list.html"
    model = Product
    context_object_name = "product_list"
    paginate_by = 36

    def get_queryset(self):
        search = self.request.GET.get('search', False)
        if search:
            object_list = Product.objects.filter(Q(title__icontains=search) | Q(category__title__icontains=search) |
                                                 Q(brand__icontains=search)).order_by('-price')
            if object_list.exists():
                messages.add_message(self.request, messages.SUCCESS, f'{object_list.count()} Ürün Bulundu.')
                return object_list
            else:
                messages.add_message(self.request, messages.ERROR, 'Aradığınız Ürün Bulunamadı')
                return self.model.objects.all().order_by('-price')
        else:
            object_list = self.model.objects.all().order_by('-price')

            return object_list

    def get_context_data(self, **kwargs):
        context = super(SortByHighPriceView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            cart_id = self.request.session.session_key
            context['wish_list_products'] = Product.objects.filter(wish_list__username=self.request.user)
            context['cart_list'] = CartItems.objects.filter(cart__cart_id=cart_id).aggregate(Sum('quantity'))[
                'quantity__sum']
        return context


class NewestProductsView(ListView):
    template_name = "pages/store_list.html"
    model = Product
    context_object_name = "product_list"
    paginate_by = 36
    ordering = ['-created']

    def get_queryset(self):
        search = self.request.GET.get('search', False)
        product_list = Product.objects.annotate(num_likes=Count('likes')).order_by('-num_likes')
        if search:
            return product_list.filter(Q(title__icontains=search) | Q(category__title__icontains=search) |
                                       Q(brand__icontains=search))
        else:
            return product_list

    def get_context_data(self, **kwargs):
        context = super(NewestProductsView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            cart_id = self.request.session.session_key
            context['wish_list_products'] = Product.objects.filter(wish_list__username=self.request.user)
            context['cart_list'] = CartItems.objects.filter(cart__cart_id=cart_id).aggregate(Sum('quantity'))[
                'quantity__sum']
        return context


class MostLikesProductsView(ListView):
    template_name = "pages/store_list.html"
    model = Product
    context_object_name = "product_list"
    paginate_by = 36

    def get_queryset(self):
        search = self.request.GET.get('search', False)
        product_list = Product.objects.annotate(num_likes=Count('likes')).order_by('-num_likes')
        if search:
            return product_list.filter(Q(title__icontains=search) | Q(category__title__icontains=search) |
                                       Q(brand__icontains=search))
        else:
            return product_list

    def get_context_data(self, **kwargs):
        context = super(MostLikesProductsView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            cart_id = self.request.session.session_key
            context['wish_list_products'] = Product.objects.filter(wish_list__username=self.request.user)
            context['cart_list'] = CartItems.objects.filter(cart__cart_id=cart_id).aggregate(Sum('quantity'))[
                'quantity__sum']
        return context


class MostViewedProductsView(ListView):
    template_name = "pages/store_list.html"
    model = Product
    context_object_name = "product_list"
    paginate_by = 36

    def get_queryset(self):
        search = self.request.GET.get('search', False)
        object_list = Product.objects.order_by('-hit_count__hits')
        if search:
            object_list = object_list.filter(Q(title__icontains=search) | Q(category__title__icontains=search) |
                                             Q(brand__icontains=search)).order_by(
                '-hit_count__hits')
            messages.add_message(self.request, messages.SUCCESS, f'{object_list.count()} Ürün Bulundu.')

        return object_list

    def get_context_data(self, **kwargs):
        context = super(MostViewedProductsView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            cart_id = self.request.session.session_key
            context['wish_list_products'] = Product.objects.filter(wish_list__username=self.request.user)
            context['cart_list'] = CartItems.objects.filter(cart__cart_id=cart_id).aggregate(Sum('quantity'))[
                'quantity__sum']
        return context


class DiscountProductsView(ListView):
    template_name = "pages/store_list.html"
    model = Product
    context_object_name = "product_list"
    paginate_by = 36

    def get_queryset(self):
        search = self.request.GET.get('search', False)

        object_list = Product.objects.filter(is_discount=True)

        if search:
            object_list = object_list.filter(Q(title__icontains=search) | Q(category__title__icontains=search) |
                                             Q(brand__icontains=search))

            messages.add_message(self.request, messages.SUCCESS, f'{object_list.count()} Ürün Bulundu.')

        return object_list

    def get_context_data(self, **kwargs):
        context = super(DiscountProductsView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            cart_id = self.request.session.session_key
            context['wish_list_products'] = Product.objects.filter(wish_list__username=self.request.user)
            context['cart_list'] = CartItems.objects.filter(cart__cart_id=cart_id).aggregate(Sum('quantity'))[
                'quantity__sum']
        return context


def product_likes(request, pk):
    if request.user.is_anonymous:
        messages.error(request, "Lütfen giriş yapınız")
        return redirect('%s?next=/blog/' % settings.LOGIN_URL)
    else:
        product = Product.objects.get(pk=pk)
        if product.likes.filter(id=request.user.id).exists():
            messages.add_message(request, messages.WARNING, f"{product.title} zaten beğenmişsiniz")
            if product.dislikes.filter(id=request.user.id).exists():
                product.dislikes.remove(request.user)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        elif product.dislikes.filter(id=request.user.id).exists():
            product.dislikes.remove(request.user)
            product.likes.add(request.user)
            messages.add_message(request, messages.INFO, f"Karar değiştirip {product.title} ürünü beğendiniz")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        product.likes.add(request.user)
        messages.add_message(request, messages.SUCCESS, f"{product.title} beğendiniz")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def product_dislikes(request, pk):
    if request.user.is_anonymous:
        messages.error(request, "Lütfen giriş yapınız")
        return redirect('%s?next=/blog/' % settings.LOGIN_URL)
    else:
        product = Product.objects.get(pk=pk)
        if product.dislikes.filter(id=request.user.id).exists():
            messages.add_message(request, messages.WARNING, f"{product.title} zaten beğenmedinizi biliyoruz :) ")
            if product.likes.filter(id=request.user.id).exists():
                product.likes.remove(request.user)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        elif product.likes.filter(id=request.user.id).exists():
            product.likes.remove(request.user)
            product.dislikes.add(request.user)
            messages.add_message(request, messages.INFO, f"Karar değiştirip {product.title} ürünü beğenmediniz")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        product.dislikes.add(request.user)
        messages.add_message(request, messages.ERROR, f"{product.title} ürünü beğenmediniz")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def wish_list(request, pk):
    if request.user.is_anonymous:
        messages.error(request, "Lütfen giriş yapınız")
        return redirect('%s?next=' % settings.LOGIN_URL)

    else:
        product = Product.objects.get(pk=pk)
        if product.wish_list.filter(id=request.user.id).exists():
            product.wish_list.remove(request.user)
            messages.add_message(request, messages.ERROR, f"{product.title} ürünü istek listesinden kaldırdınız")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        product.wish_list.add(request.user)
        messages.add_message(request, messages.SUCCESS, f"{product.title} ürünü istek listesine eklediniz")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def comment_delete(request, pk):
    try:
        comment = ProductComments.objects.get(pk=pk)
    except ProductComments.DoesNotExist:
        messages.add_message(request, messages.SUCCESS, f"Yetkisiz işlem")
        return redirect("store:store_home")

    if request.user.is_anonymous:
        messages.error(request, "Lütfen giriş yapınız")
        return redirect(f"{settings.LOGIN_URL}?next=/")

    if comment.user != request.user:
        messages.add_message(request, messages.SUCCESS, f"Yetkisiz işlem")
        return redirect("store:store_home")

    comment.delete()
    messages.add_message(request, messages.SUCCESS, f"{comment.comment} yorumunuz silindi")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def report_comment(request, pk):
    comment = ProductComments.objects.get(pk=pk)
    comment.report_count += 1
    comment.save()
    messages.add_message(request, messages.INFO, "Yorum rapor edildi ve incelenecek")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def add_cart(request, pk, cart_id):
    if request.user.is_anonymous:
        messages.error(request, "Lütfen Giriş Yapınız")
        return redirect('%s?next=/magaza/products/' % settings.LOGIN_URL)

    else:
        product = Product.objects.get(pk=pk)
        customer = Profile.objects.get(user=request.user)

        if product.stock == 0:
            messages.info(request, "Ürün stoklarda kalmamıştır.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        try:
            cart = Cart.objects.get(cart_id=cart_id)
        except:
            cart = Cart.objects.create(cart_id=cart_id, customer=customer)

        try:
            cart_item = CartItems.objects.get(product=product, cart=cart)
            cart_item.quantity += 1

            if product.is_discount:
                cart_item.items_total = round(cart_item.quantity * cart_item.product.discount_price, 2)
            else:
                cart_item.items_total = round(cart_item.quantity * cart_item.product.price, 2)
            cart_item.save()

        except CartItems.MultipleObjectsReturned:
            cart_item = CartItems.objects.filter(product=product, cart=cart)
            for item in cart_item:
                if item.product.pk == product.pk:
                    item.quantity += 1
                    if product.is_discount:
                        cart_item.items_total = round(item.quantity * item.product.discount_price, 3)
                    else:
                        cart_item.items_total = round(item.quantity * item.product.price, 3)
                    item.save()

        except CartItems.DoesNotExist:
            cart_item = CartItems.objects.create(
                product=product,
                quantity=1,
                cart=cart
            )

            if product.is_discount:
                cart_item.items_total = round(cart_item.quantity * cart_item.product.discount_price, 3)
            else:
                cart_item.items_total = round(cart_item.quantity * cart_item.product.price, 3)

            cart_item.save()

        messages.success(request, "Ürün sepetinize eklendi")

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def MyCartView(request, user, cart_id):
    cart_total_price = 0
    total = 0
    if request.user.is_anonymous:
        messages.error(request, "Lütfen giriş yapınız")
        return redirect('%s?next=' % settings.LOGIN_URL)

    my_cart_list = CartItems.objects.filter(cart__cart_id=cart_id)
    valid_cart_list = CartItems.objects.filter(cart__cart_id=cart_id, is_valid=True)
    cart_total_products = CartItems.objects.filter(cart__cart_id=cart_id).aggregate(Sum('quantity'))['quantity__sum']
    wish_list_products = Product.objects.filter(wish_list__username=request.user)
    cart = Cart.objects.get(cart_id=cart_id)

    for items in my_cart_list:
        if items.product.is_discount:
            items.items_total = items.quantity * items.product.discount_price
        else:
            items.items_total = items.quantity * items.product.price
        items.save()

    if my_cart_list.count() != 0:
        cart_total_price = CartItems.objects.filter(cart__cart_id=cart_id).aggregate(Sum('items_total'))[
            'items_total__sum']
        cart.total = round(cart_total_price, 1)
        cart.save()

    if request.user.is_authenticated:
        cart_list = CartItems.objects.filter(cart__cart_id=cart_id).aggregate(Sum('quantity'))[
            'quantity__sum']

    if cart.app_promo is True:
        cart.app_promo = False
        cart.save()

    context = {
        'my_cart_list': my_cart_list, 'cart_total_products': cart_total_products,
        'cart_total_price': round(cart_total_price, 3), 'valid_cart_list': valid_cart_list,
        'cart_id': cart_id, "wish_list_products": wish_list_products, "total": total, 'cart_list': cart_list
    }

    return render(request, 'pages/my_cart.html', context)


def WishListView(request, user):
    total = 0
    dis_total = 0
    wish_list = Product.objects.filter(wish_list__username=request.user)
    profile = Profile.objects.get(user=request.user)

    cart_list = CartItems.objects.filter(cart__cart_id=request.session.session_key, cart__customer=profile).aggregate(
        Sum('quantity'))['quantity__sum']

    wish_list_products = Product.objects.filter(wish_list__username=profile)

    if wish_list.filter(is_discount=False):
        total = wish_list.aggregate(Sum('price'))['price__sum']

    elif wish_list_products.filter(is_discount=True):
        dis_total = wish_list.aggregate(Sum('discount_price'))['discount_price__sum']

    return render(request, "pages/wish_list.html", {'wish_list': wish_list, 'total': total, "cart_list": cart_list,
                                                    "wish_list_products": wish_list_products, 'dis_total': dis_total})


def remove_item_wishlist(request, pk):
    product = Product.objects.get(pk=pk)
    product.wish_list.remove(request.user)
    messages.success(request, "Ürünü istek listesinden çıkarttınız")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def UpdateMyCart(request, pk):
    if request.user.is_anonymous:
        messages.error(request, "Lütfen giriş yapınız")
        return redirect('%s?next=' % settings.LOGIN_URL)
    product = CartItems.objects.get(product_id=pk)
    quantity = request.GET.get('quantity', )
    product.quantity = int(quantity)
    if product.product.is_discount:
        product.total = product.quantity * product.product.discount_price
    else:
        product.total = product.quantity * product.product.price
    product.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def remove_product_from_cart(request, pk):
    if request.user.is_anonymous:
        messages.error(request, "Lütfen giriş yapınız")
        return redirect('%s?next=' % settings.LOGIN_URL)
    try:
        product = CartItems.objects.get(product__pk=pk)
    except:
        product = CartItems.objects.filter(cart__customer__user=request.user, product__pk=pk).first()

    product.delete()

    messages.success(request, "Ürünü sepetten çıkarttınız")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def valid_cart(request, cart_id):
    cart = CartItems.objects.filter(cart__cart_id=cart_id, cart__customer__user=request.user)
    cart.update(is_valid=True)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def non_valid_cart(request, cart_id):
    cart = CartItems.objects.filter(cart__cart_id=cart_id, cart__customer__user=request.user)
    cart.update(is_valid=False)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def add_non_valid_my_cart(request, pk, cart_id):
    cart = CartItems.objects.get(cart__cart_id=cart_id, product__pk=pk, is_valid=False)
    cart.quantity += 1
    if cart.product.stock < cart.quantity:
        messages.error(request, "Ürün stokta kalmamıştır.")
        cart.quantity = cart.product.stock
    if cart.product.is_discount:
        cart.items_total = round(cart.quantity * cart.product.discount_price, 3)
    else:
        cart.items_total = round(cart.quantity * cart.product.price, 3)
    if cart.quantity <= 0:
        cart.quantity = 1

    cart.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def remove_non_valid_my_cart(request, pk, cart_id):
    cart = CartItems.objects.get(cart__cart_id=cart_id, product__pk=pk, is_valid=False)
    if cart.quantity <= 1:
        cart.quantity = 1

    else:
        cart.quantity -= 1

    if cart.product.is_discount:
        cart.items_total = round(cart.quantity * cart.product.discount_price, 3)
    else:
        cart.items_total = round(cart.quantity * cart.product.price, 3)
    cart.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def checkout_view(request, user, cart_id):
    total = 0
    if request.user.is_anonymous:
        messages.error(request, "Lütfen giriş yapınız")
        return redirect('%s?next=' % settings.LOGIN_URL)

    profile = Profile.objects.get(user=request.user)

    checkout_form = CheckOutForm(request.POST or None, instance=profile)

    promo_form = PromoCodeForm(request.POST or None)

    cart = Cart.objects.get(cart_id=cart_id)

    my_cart_list = CartItems.objects.filter(cart__cart_id=cart_id)
    cart_total_products = my_cart_list.aggregate(Sum('quantity'))['quantity__sum']
    cart_total_price = my_cart_list.aggregate(Sum('items_total'))['items_total__sum']

    discount = round(cart.total - cart_total_price, 3)

    if request.method == "POST":
        if checkout_form.is_valid():
            form = checkout_form.save(commit=False)
            form.save()

    if my_cart_list.count() == 0:
        messages.error(request, "Ürün sepeniz boş")
        return redirect('store:store_home')

    price = \
        Product.objects.filter(wish_list__username=request.user, is_discount=False).aggregate(
            Sum('price'))[
            'price__sum']
    discount_price = \
        Product.objects.filter(wish_list__username=request.user, is_discount=True).aggregate(
            Sum('discount_price'))['discount_price__sum']

    if discount_price is not None and price is not None:
        total = discount_price + price
    elif discount_price is not None and price is None:
        total = discount_price
    elif discount_price is None and price is not None:
        total = price

    total = round(total, 3)

    wish_list_products = Product.objects.filter(wish_list__username=request.user)

    context = {'my_cart_list': my_cart_list, 'cart_total_products': cart_total_products,
               'cart_total_price': round(cart_total_price, 3), 'form': checkout_form, 'cart_list': cart_total_products,
               'promo_form': promo_form, 'cart_id': cart_id, 'cart': cart, 'dis': discount, "total": total,
               "wish_list_products": wish_list_products
               }

    return render(request, "pages/check_out.html", context)


def PromoCodeView(request, user, cart_id):
    if request.user.is_anonymous:
        messages.error(request, "Lütfen giriş yapınız")
        return redirect('%s?next=' % settings.LOGIN_URL)

    my_cart_list = CartItems.objects.filter(cart__cart_id=cart_id)
    cart_total_products = my_cart_list.aggregate(Sum('quantity'))['quantity__sum']
    cart_total_price = my_cart_list.aggregate(Sum('items_total'))['items_total__sum']

    cart = Cart.objects.get(cart_id=cart_id)

    promo_code = request.GET.get('promote_code', False)

    if promo_code:
        if PromoCodeModel.objects.exists():
            for code in PromoCodeModel.objects.all():
                if promo_code == code.promo_code and code.promo_end_date >= now():
                    if cart.customer != code.customer and cart.app_promo is False:
                        if code.promo_type == "per":

                            total = round(float(cart.total) - float(cart_total_price) * (int(code.promo) / 100), 3)

                        else:
                            total -= round(cart_total_price - code.promo, 3)

                        cart.total = total
                        cart.app_promo = True
                        cart.promo = promo_code
                        cart.save()

                    else:
                        messages.error(request, 'Kampanyaya zaten katılmışsınız')
                        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

                else:
                    messages.error(request, 'Hatalı İndirim kodu')
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        else:
            messages.error(request, "Hatalı indirim kodu")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def SubscribeView(request):
    email = request.GET.get('email', False)
    if Subscribe.objects.exists():
        for sub_email in Subscribe.objects.all():
            if sub_email.email == email:
                messages.error(request, "Zaten Abonesiniz")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if email.endswith('edu.tr') or email.endswith('gmail.com') or email.endswith(
                'windowslive.com') or email.endswith('hotmail.com') or email.endswith('yahoo.com'):

            Subscribe.objects.create(email=email)
            messages.success(request, "Başarılı şekilde Abone oldunuz")
        else:
            messages.error(request,
                           "edu.tr, gmail.com, windowslive.com, hotmail.com yada yahoo.com adresleri olmalıdır")


    else:
        Subscribe.objects.create(email=email)
        messages.success(request, "Başarılı şekilde Abone oldunuz")

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def unsubscribe(request, unsubscribe_email):
    unsubscribe_item = Subscribe.objects.get(email=unsubscribe_email)
    unsubscribe_item.delete()
    messages.success(request, "Email aboneliğinden çıktınız.")
    return redirect('store:store_home')


def contact(request):
    try:
        neumorphism = SiteSettingModels.objects.filter(is_active=True).get(theme__icontains='neumorphism')
    except SiteSettingModels.DoesNotExist:
        neumorphism = False
    form = ContactForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            instance = form.save(commit=False)
            try:

                template_name = os.path.join(settings.BASE_DIR, "templates", 'pages', "contact_email.html")
                template = get_template(template_name)
                context = {"subject": instance.subject, 'name': instance.name, 'email': instance.email,
                           'message': instance.message, }
                html_content = template.render(context)
                body = HttpResponse(html_content).content.decode("utf-8")
                msg = EmailMultiAlternatives(
                    subject='Kullanıcı iletişim için yazdı',
                    body=body,
                    from_email=settings.EMAIL_HOST_USER,
                    to=[settings.EMAIL_HOST_USER],
                )
                msg.content_subtype = "html"
                msg.send()

            except SMTPAuthenticationError as smtp_error:  # Özel olarak SMTPAuthenticationError için

                messages.error(request, f"Giriş yetkilendirme hatası: {smtp_error}")

            except Exception as e:

                messages.error(request, f"{str(e)}")

            messages.success(request, "Mesajınız gönderildi. En kısa sürede email adrenize cevap yazacağız.")

            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return render(request, 'pages/contact.html', {'form': form, 'neumorphism': neumorphism})
