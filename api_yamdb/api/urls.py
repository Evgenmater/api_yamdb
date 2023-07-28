from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (
    UserViewSet, APISignUp, APIToken)

router_v1 = DefaultRouter()
router_v1.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/', include('djoser.urls')),
    path('v1/auth/', include('djoser.urls.jwt')),
    path('v1/auth/signup/', APISignUp.as_view()),
    path('v1/auth/token/', APIToken.as_view()),
]
