from django.urls import include, path
from drf_spectacular.views import (SpectacularAPIView, SpectacularRedocView,
                                   SpectacularSwaggerView)
from rest_framework.routers import DefaultRouter

from .views import AccessOnlyTokenView, OrderViewSet, UserViewSet, signup

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('orders', OrderViewSet, basename='orders')

auth_urls = [
    path('signup/', signup, name='signup'),
    path('token/', AccessOnlyTokenView.as_view(), name='token'),
]

spectacular_urls = [
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(), name='swagger'),
    path('redoc/', SpectacularRedocView.as_view(), name='redoc'),
]

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include(auth_urls)),
    path('', include(spectacular_urls)),
]
