from django.contrib import admin 
from django.urls import path, include 

admin.site.site_header = "INVENTORY STORE"
admin.site.index_title = "Admin"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('invApp.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]