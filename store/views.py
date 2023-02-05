from .models import Product, Category, ProductDetailsModel, HeaderSlideModel, \
    GalleryModel, Comments, ProductOptionsNameModel, ProductOptions
from django.views import generic
from hitcount.views import HitCountDetailView
from django.db.models import Q
from django.shortcuts import redirect, get_object_or_404

from django.http import HttpResponseRedirect
from django.contrib import messages
from carts.models import CartItems
from django.db.models import Sum


class HomeView(generic.ListView):
    template_name = 'pages/home.html'
    model = Product

    def get(self, request, *args, **kwargs):
        search = self.request.GET.get('arama', False)
        if search:
            return redirect('magaza/products/?arama=%s' % (search))
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return Product.objects.order_by('-hit_count__hits').filter(is_available='SV')[:16]

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['slides'] = HeaderSlideModel.objects.all()
        if self.request.user.is_authenticated:
            context['cart_items'] = CartItems.objects.filter(cart__customer=self.request.user.pk)
            context['my_favorites'] = Product.objects.filter(likes=self.request.user)
            total = CartItems.objects.filter(cart__customer=self.request.user.pk).aggregate(Sum('total'))
            context['total'] = total.get('total__sum')
        return context


class ProductDetailView(HitCountDetailView, generic.DetailView):
    template_name = 'pages/detail.html'
    model = Product
    count_hit = True

    def get(self, request, *args, **kwargs):
        search = self.request.GET.get('arama', False)
        if search:
            return redirect('%s?next=arama=%s' % (self.request.path, search))
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        comment = request.POST.get('comment')

        if comment:
            comment = Comments(comment=comment,
                               commentator=self.request.user,
                               rating=request.POST.get('rating'),
                               product=self.get_object())
            comment.save()
            messages.success(request, "Yorumunuz başarılı bir şekilde eklendi")
            return HttpResponseRedirect(self.request.build_absolute_uri())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = get_object_or_404(Product, slug=self.kwargs['slug'])
        context['comments'] = product.comment.all().order_by('-id')
        if ProductDetailsModel.objects.exists():
            context['options'] = ProductDetailsModel.objects.filter(product=self.get_object().pk)
        if ProductOptionsNameModel.objects.exists():
            context['product_options'] = ProductOptions.objects.filter(option_name__product=self.get_object().pk)
        if self.request.user.is_authenticated:
            context['cart_items'] = CartItems.objects.filter(cart__customer=self.request.user.pk)
            total = CartItems.objects.filter(cart__customer=self.request.user.pk).aggregate(Sum('total'))
            context['total'] = total.get('total__sum')
            context['my_favorites'] = Product.objects.filter(likes=self.request.user)
        return context


class AllProductsView(generic.ListView):
    template_name = 'pages/allproducts.html'
    model = Product
    paginate_by = 20

    def get_queryset(self):
        search = self.request.GET.get('arama', False)
        if search:
            return Product.objects.filter(Q(title__icontains=search))
        else:
            return Product.objects.order_by('-created').filter(is_available='SV')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categoriys'] = Category.objects.all()
        if self.request.user.is_authenticated:
            context['cart_items'] = CartItems.objects.filter(cart__customer=self.request.user.pk)
            total = CartItems.objects.filter(cart__customer=self.request.user.pk).aggregate(Sum('total'))
            context['total'] = total.get('total__sum')
            context['my_favorites'] = Product.objects.filter(likes=self.request.user)
        return context


class GalleriListView(generic.ListView):
    template_name = 'pages/galery.html'
    model = GalleryModel

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categoriys'] = Category.objects.all()
        if self.request.user.is_authenticated:
            context['cart_items'] = CartItems.objects.filter(cart__customer=self.request.user.pk)
            total = CartItems.objects.filter(cart__customer=self.request.user.pk).aggregate(Sum('total'))
            context['total'] = total.get('total__sum')
            context['my_favorites'] = Product.objects.filter(likes=self.request.user)
        return context
