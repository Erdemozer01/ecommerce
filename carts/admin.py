from django.contrib import admin
from .models import Cart, CartItems



class CartItemsInline(admin.TabularInline):
    model = CartItems


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['customer', 'cart_id', 'created']
    list_filter = ['customer', 'created']
    search_fields = ['customer', 'cart_id', ]
    inlines = [
        CartItemsInline
    ]
