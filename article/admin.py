from django.contrib import admin
from .models import Category, Posts, ArticleImages, ArticleTags


class ArticleImagesAdmin(admin.TabularInline):
    model = ArticleImages
    extra = 1
    classes = ['collapse']
    ordering = ['-created']


class ArticleTagsAdmin(admin.TabularInline):
    model = ArticleTags
    extra = 1
    classes = ['collapse']
    ordering = ['-created']

    readonly_fields = ['created']



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'created']
    search_fields = ['title', 'explain']


@admin.register(Posts)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'created']
    list_filter = ['author', 'category', 'created']
    search_fields = ['title', 'author']
    search_help_text = "Başlık ve yazara göre arama"
    inlines = [ArticleImagesAdmin, ArticleTagsAdmin]