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
    """
    Регистрация нового пользователя.
    Создает нового пользователя в системе.
    Возвращает данные созданного пользователя (без пароля).
    """
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
    """
    Получение JWT токена для аутентификации.
    Принимает username/email и пароль.
    Возвращает access токен.
    """
    serializer_class = AccessOnlyTokenSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления пользователями.
    Доступен только администраторам для управления всеми пользователями.
    Обычные пользователи могут работать со своим профилем через /users/me/.
    """
    serializer_class = UserSerializer
    lookup_field = 'username'
    http_method_names = ('get', 'post', 'patch', 'delete')
    permission_classes = (IsAdminUser,)

    def get_queryset(self):
        """Возвращает пользователей с вычисленным возрастом."""
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
        methods=('get', 'patch', 'delete'),
        url_path=settings.PROFILE_URL_SEGMENT,
        permission_classes=(IsAuthenticated,),
        serializer_class=CurrentUserSerializer,
    )
    def current_user(self, request):
        """
        Управление профилем текущего пользователя.
        GET: Получить данные своего профиля
        PATCH: Обновить данные своего профиля
        DELETE: Удалить свой аккаунт
        Доступно любому аутентифицированному пользователю.
        """
        user = request.user
        if request.method == 'GET':
            return Response(
                CurrentUserSerializer(user).data,
                status=status.HTTP_200_OK,
            )
        if request.method == 'DELETE':
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        serializer = CurrentUserSerializer(
            user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrderViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления заказами.
    Аутентифицированные пользователи видят только свои заказы.
    Администраторы видят все заказы и дополнительную информацию.
    """
    permission_classes = (IsOrdererOrAdmin,)

    def get_serializer_class(self):
        """Возвращает подходящий сериализатор в зависимости от пользователя."""
        if self.request.user.is_staff and self.action != 'create':
            return OrderSerializer
        return OrderShortSerializer

    def get_queryset(self):
        """Возвращает заказы в зависимости от прав пользователя."""
        if self.request.user.is_staff:
            return Order.objects.select_related('user')
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Автоматически привязывает заказ к текущему пользователю."""
        serializer.save(user=self.request.user)

    @action(
        detail=False,
        url_path=USERNAME_PATH_PARAM_REGEX,
        methods=('get',),
        permission_classes=(IsAdminUser,)
    )
    def orders_by_username(self, request, username):
        """
        Получение заказов конкретного пользователя.
        Доступно только администраторам.
        Возвращает все заказы указанного пользователя.
        """
        serializer = self.get_serializer(
            self.get_queryset()
            .filter(user=get_object_or_404(User, username=username)),
            many=True
        )
        return Response(serializer.data)
