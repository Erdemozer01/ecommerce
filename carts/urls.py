from django.urls import path
from . import views

app_name = 'carts'

urlpatterns = [
    path('<str:user>/', views.CartListView.as_view(), name='sepetim'),
    path('<user>/<product_code>/', views.add_cart, name='add_cart'),
    path('delete/<user_id>/<product_code>/', views.delete_item_cart, name='delete_item'),
]
