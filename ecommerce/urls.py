from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from store.views import HomeView

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('ckeditor/', include('ckeditor_uploader.urls')),
                  path('accounts/', include('django.contrib.auth.urls')),
                  path('', include('accounts.urls', namespace='accounts')),
                  path('hitcount/', include('hitcount.urls', namespace='hitcount')),
                  path('magaza/', include('store.urls', namespace='store')),
                  path('', HomeView.as_view(), name='anasayfa'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
