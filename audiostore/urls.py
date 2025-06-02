from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('catalog/', include('catalog.urls', namespace='catalog')),
    path('labs/', include('labs.urls', namespace='labs')),
    path('hitcount/', include('hitcount.urls', namespace='hitcount')),
    path('lab3/', include('lab3.urls')),
    path('lab4/', include('lab4.urls')),
    path('lab5/', include('lab5.urls')),
    path('lab6/', include('lab6.urls')),


]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)