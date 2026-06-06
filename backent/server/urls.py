from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shop.urls')),  # Ҳамаи роҳҳоро аз папкаи shop мехонад
]

# Шарти DEBUG-ро гирифтем, то дар PythonAnywhere ҳам суратҳо 100% бароянд:
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)