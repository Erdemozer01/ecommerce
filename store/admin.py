from django.contrib import admin
from .models import Product, Category, ProductOptionsModel, HeaderSlideModel, GalleryModel, GalleryCategoryChildModel


class GaleriInline(admin.TabularInline):
    model = GalleryModel


@admin.register(GalleryCategoryChildModel)
class GalleryModelAdmin(admin.ModelAdmin):
    inlines = [GaleriInline]


@admin.register(HeaderSlideModel)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'subtitle', 'created']
    search_fields = ['title']


class ProductOptionsInline(admin.TabularInline):
    model = ProductOptionsModel


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'created']
    search_fields = ['title', 'explain']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'brand', 'label', 'price', 'new_price', 'stock', 'is_available', 'created']
    list_filter = ['created', 'updated', 'label', 'is_available', ]
    search_fields = ['title', 'category__title', 'label']
    search_help_text = 'Başlık ve Etikete göre arama'
    list_editable = ['stock', 'new_price', 'is_available']
    inlines = [ProductOptionsInline]

    fieldsets = (
        ('Ürün Bilgileri', {
            'fields': (
                'category', 'title', 'text', 'brand', 'price', 'new_price', 'stock', 'is_available', 'label')
        }),
        ('Ürün Görselleri', {
            'classes': ('wide', 'extrapretty'),
            'fields': ('image1', 'image2', 'image3'),
        }),
        ('Beğeniler', {
            'classes': ('collapse ', 'extrapretty'),
            'fields': ('likes',),
        }),
    )
