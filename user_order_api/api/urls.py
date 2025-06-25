from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AccessOnlyTokenView, OrderViewSet, UserViewSet, signup

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('orders', OrderViewSet, basename='orders')

auth_urls = [
    path('signup/', signup, name='signup'),
    path('token/', AccessOnlyTokenView.as_view(), name='token'),
]

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include(auth_urls)),
]
