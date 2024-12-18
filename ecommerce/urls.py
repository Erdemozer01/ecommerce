from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django_ckeditor_5.views import upload_file
from article.views import post_likes, post_dislikes

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('hitcount/', include('hitcount.urls', namespace='hitcount')),
    path("ckeditor5/", include('django_ckeditor_5.urls')),
    path("ckeditor5_upload_file/", upload_file, name="ckeditor5_upload_file"),
    path('', include('store.urls', namespace='store')),
    path("gallery-handler/", include("galleryfield.urls")),
    path('makale/', include('article.urls', namespace='article')),
    path('post-likes/<int:pk>/', post_likes, name='post_likes'),
    path('post-dislikes/<int:pk>/', post_dislikes, name='post_dislikes'),
    path('accounts/', include('accounts.urls', namespace="accounts")),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += staticfiles_urlpatterns()

admin.site.site_title = "E-Commerce"

admin.site.site_header = "E-Commerce Admin Panel"
