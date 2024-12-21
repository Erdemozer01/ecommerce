from django.urls import path
from .views import (
    StoreListView, ProductDetailView, ProductCategoryView, product_likes, product_dislikes, wish_list, \
    SortByLowPriceView, SortByHighPriceView, NewestProductsView, comment_delete, report_comment,
    MostLikesProductsView, BrandCategoryView, add_cart, MyCartView, UpdateMyCart, remove_product_from_cart,
    MostViewedProductsView, checkout_view, PromoCodeView, valid_cart, non_valid_cart, add_non_valid_my_cart,
    remove_non_valid_my_cart, SubscribeView, unsubscribe, contact, WishListView, remove_item_wishlist
)

app_name = 'store'

urlpatterns = [
    path('', StoreListView.as_view(), name='store_home'),
    path('<int:pk>/<str:brand>/<str:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('product-kategori/<str:category>/', ProductCategoryView.as_view(), name='product_category'),
    path('product-marka-kategori/<str:brand>/', BrandCategoryView.as_view(), name='brand_category'),
    path('like/<pk>/', product_likes, name='product_likes'),
    path('dislike/<pk>/', product_dislikes, name='product_dislikes'),
    path('add-wish-list/<pk>/', wish_list, name='wish_list'),
    path('sırala/düsuk-fiyattan-yüksek-fiyata/', SortByLowPriceView.as_view(), name='sort_low_price'),
    path('sırala/yüksek-fiyattan-düşük-fiyata/', SortByHighPriceView.as_view(), name='sort_high_price'),
    path('sırala/en-çok-begenilen-ürünler/', MostLikesProductsView.as_view(), name='most_likes_products'),
    path('sırala/yeni-gelenden-eskiye/', NewestProductsView.as_view(), name='newest_products'),
    path('sırala/most-viewed-products/', MostViewedProductsView.as_view(), name='most_viewed_products'),
    path('comment-delete/<pk>/', comment_delete, name='comment_delete'),
    path('report/<pk>/', report_comment, name='report_comment'),
    path('add-cart/<pk>/<cart_id>/', add_cart, name='add_cart'),
    path('sepetim/<user>/<cart_id>/', MyCartView, name='my_cart_list'),
    path('update-my-cart/<int:pk>/', UpdateMyCart, name='update_my_cart'),
    path('valid_my_cart/<cart_id>/', valid_cart, name='valid_my_cart'),
    path('non_valid_cart/<cart_id>/', non_valid_cart, name='non_valid_cart'),
    path('add_non_valid_my_cart/<pk>/<cart_id>/', add_non_valid_my_cart, name='add_non_valid_my_cart'),
    path('remove_non_valid_my_cart/<pk>/<cart_id>/', remove_non_valid_my_cart, name='remove_non_valid_my_cart'),
    path('remove_product_from_cart/<int:pk>/', remove_product_from_cart, name='remove_product_from_cart'),
    path('checkout-cart/<user>/<cart_id>/', checkout_view, name='checkout_view'),
    path('promo-code/<user>/<cart_id>/', PromoCodeView, name='promo_code'),
    path('abone-ol/', SubscribeView, name='abone_ol'),
    path('unsubscribe/<unsubscribe_email>/', unsubscribe, name='unsubscribe'),
    path('iletişim/', contact, name='contact'),
    path('istek-listem/<user>/', WishListView, name='my_wish_list'),
    path('istek-listesinden-çıkart/<pk>/', remove_item_wishlist, name='remove_wish_list'),
]
