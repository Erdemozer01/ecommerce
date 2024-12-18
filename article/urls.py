from django.urls import path

from .views import ArticleListView, ArticleDetailView, ArticleCategoryView, ArticleTagsView

app_name = 'article'

urlpatterns = [
    path('', ArticleListView.as_view(), name='article_home'),
    path('<int:pk>/<str:category>/<str:slug>/', ArticleDetailView.as_view(), name='article_detail'),
    path('<str:category>/', ArticleCategoryView.as_view(), name='article_category'),
    path('etiketler/<tags>/', ArticleTagsView.as_view(), name='article_tags'),
]
