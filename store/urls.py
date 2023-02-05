from django.urls import path
from .views import ProductDetailView, AllProductsView, GalleriListView

app_name = 'store'

urlpatterns = [
    path('<slug:category>/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('products/', AllProductsView.as_view(), name='all_products'),
    path('galeri/', GalleriListView.as_view(), name='galeri'),
]
