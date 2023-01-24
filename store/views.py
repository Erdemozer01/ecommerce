from .models import Product, Category, ProductOptionsModel, HeaderSlideModel, GalleryModel
from django.views import generic
from hitcount.views import HitCountDetailView
from django.db.models import Q
from django.shortcuts import redirect


class HomeView(generic.ListView):
    template_name = 'pages/home.html'
    model = Product

    def get(self, request, *args, **kwargs):
        search = self.request.GET.get('arama', False)
        if search:
            return redirect('magaza/urunler/?arama=%s' % (search))
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return Product.objects.order_by('-hit_count__hits').filter(is_available='SV')[:16]

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['slides'] = HeaderSlideModel.objects.all()
        return context


class ProductDetailView(HitCountDetailView, generic.DetailView):
    template_name = 'pages/detail.html'
    model = Product
    count_hit = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if ProductOptionsModel.objects.exists():
            context['options'] = ProductOptionsModel.objects.filter(product=self.get_object().pk)
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
        return context


class GalleriListView(generic.ListView):
    template_name = 'pages/galery.html'
    model = GalleryModel