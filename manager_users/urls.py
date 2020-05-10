from django.contrib import admin
from django.urls import path, re_path, include


urlpatterns = [
    path('admin/', admin.site.urls),

	#path to our account's app endpoints
    re_path(r'^', include('users.urls')),
]