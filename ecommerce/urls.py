from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from store.views import HomeView
from carts.views import FavoriteListView, delete_item_favorite, add_favorite

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('ckeditor/', include('ckeditor_uploader.urls')),
                  path('accounts/', include('django.contrib.auth.urls')),
                  path('', include('accounts.urls', namespace='accounts')),
                  path('sepetim/', include('carts.urls', namespace='carts')),
                  path('hitcount/', include('hitcount.urls', namespace='hitcount')),
                  path('magaza/', include('store.urls', namespace='store')),
                  path('favorilere-ekle/<slug:slug>/', add_favorite, name='add_favorite'),
                  path('favorilerim/<user>/', FavoriteListView.as_view(), name='my_favorite'),

                  path('favorilerim/delete/<slug:slug>/', delete_item_favorite, name='delete_item_favorite'),
                  path('', HomeView.as_view(), name='anasayfa'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
