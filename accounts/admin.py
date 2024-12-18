from django.contrib import admin
from django.db.models import Sum

from .models import Profile
from store.models import Cart, CartItems


class CartItemsAdmin(admin.TabularInline):
    model = CartItems
    extra = 0
    classes = ['collapse']
    ordering = ['-created']

    def get_readonly_fields(self, request, obj=...):
        return ['product_code', 'product', 'quantity', 'product__price', 'product__discount_price', 'items_total',
                'created']


@admin.register(Cart)
class CartItemsAdmin(admin.ModelAdmin):
    inlines = [CartItemsAdmin]
    model = CartItems
    list_display = ['customer', 'cart_id', 'total', 'promo', 'app_promo', 'created']
    list_editable = ['app_promo']


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'first_name', 'last_name', 'email', 'created']
    search_fields = ['first_name', 'last_name']
    list_filter = ['created']
    ordering = ['-created']
    list_per_page = 25
