# WebAdvertising/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core.views import ComingSoonView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('accounts/', include('accounts.urls')),
    path('listings/', include('listings.urls')),
    path('payments/', include('payments.urls')),
    path('notifications/', include('notifications.urls')), 
    path('tickets/', include('tickets.urls')),
    path('coming-soon/', ComingSoonView.as_view(), name='coming_soon'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
