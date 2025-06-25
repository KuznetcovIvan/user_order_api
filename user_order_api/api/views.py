from django.conf import settings
from django.db import IntegrityError
from django.db.models import Case, IntegerField, When
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from orders.constants import USERNAME_PATH_PARAM_REGEX
from orders.models import Order, User

from .permissions import IsOrdererOrAdmin
from .serializers import (AccessOnlyTokenSerializer, CurrentUserSerializer,
                          OrderSerializer, OrderShortSerializer,
                          SignUpSerializer, UserSerializer)


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    try:
        serializer.save()
    except IntegrityError:
        raise ValidationError(
            {'email': 'email уже занят.'}
            if User.objects.filter(email=serializer.validated_data['email'])
            .exists()
            else {'username': 'username уже занят.'}
        )
    return Response(serializer.data, status=status.HTTP_201_CREATED)


class AccessOnlyTokenView(TokenObtainPairView):
    serializer_class = AccessOnlyTokenSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    lookup_field = 'username'
    http_method_names = ('get', 'post', 'patch', 'delete')
    permission_classes = (IsAdminUser,)

    def get_queryset(self):
        queryset = User.objects.annotate(
            age=Case(
                When(birth_date__isnull=False,
                     then=User.calculate_age_expression()),
                default=None,
                output_field=IntegerField(null=True)
            )
        )
        return queryset

    @action(
        detail=False,
        methods=('get', 'patch'),
        url_path=settings.PROFILE_URL_SEGMENT,
        permission_classes=(IsAuthenticated,),
        serializer_class=CurrentUserSerializer,
    )
    def current_user(self, request):
        user = request.user
        if request.method != 'PATCH':
            return Response(
                CurrentUserSerializer(user).data,
                status=status.HTTP_200_OK,
            )
        serializer = CurrentUserSerializer(
            user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, IsOrdererOrAdmin)

    def get_serializer_class(self):
        if self.request.user.is_staff and self.action != 'create':
            return OrderSerializer
        return OrderShortSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.select_related('user')
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(
        detail=False,
        url_path=USERNAME_PATH_PARAM_REGEX,
        methods=('get',),
        permission_classes=(IsAdminUser,)
    )
    def orders_by_username(self, request, username):
        serializer = self.get_serializer(
            self.get_queryset()
            .filter(user=get_object_or_404(User, username=username)),
            many=True
        )
        return Response(serializer.data)
