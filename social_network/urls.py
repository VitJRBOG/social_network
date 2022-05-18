from xml.etree.ElementInclude import include
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('social_network.apps.accounts.urls')),
    path('api/sources/', include('social_network.apps.sources.urls')),
]
