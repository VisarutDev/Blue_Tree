from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/'+'blue_tree/', include('blue_tree_api.urls')),
]
