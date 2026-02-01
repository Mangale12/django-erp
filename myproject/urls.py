from django.contrib import admin
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('hotel_app.rooms.urls')),
    path('', include('hotel_app.restaurant_menu.urls')),
    path('', include('master_setup.urls')),
    path('', include('hotel_app.reception.urls')),
    path('', include('user_management.urls')),
]

if settings.DEBUG:
    urlpatterns += [
        path('__debug__/', include('debug_toolbar.urls')),
    ]
