from django.urls import path, re_path, include
from rest_framework import routers
from .views import UserProfileViewSet

router = routers.DefaultRouter()
router.register(r'profiles', UserProfileViewSet)


urlpatterns = [
    re_path(r'^', include(router.urls)),
    re_path(r'^auth/', include('rest_auth.urls')),
    re_path(r'^auth/registration/', include('rest_auth.registration.urls'))
]