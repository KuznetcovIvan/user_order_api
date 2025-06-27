from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.db.models import Case, IntegerField, When
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema_view
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from orders.models import Order

from .filters import OrderFilter, UserFilter
from .permissions import IsOrdererOrAdmin
from .schemas import (order_create_schema, order_delete_schema,
                      order_detail_schema, order_list_schema,
                      order_patch_schema, signup_schema, token_post_schema,
                      user_delete_schema, user_destroy_schema, user_get_schema,
                      user_list_schema, user_partial_update_schema,
                      user_patch_schema, user_retrieve_schema)
from .serializers import (AccessOnlyTokenSerializer, CurrentUserSerializer,
                          OrderSerializer, OrderShortSerializer,
                          SignUpSerializer, UserSerializer)

User = get_user_model()


@signup_schema
@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    """
    Регистрация нового пользователя.
    Создает нового пользователя в системе.
    Возвращает данные созданного пользователя.
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

    @token_post_schema
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


@extend_schema_view(
    list=user_list_schema, retrieve=user_retrieve_schema,
    partial_update=user_partial_update_schema,
    destroy=user_destroy_schema,
)
class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления пользователями.
    Доступен только администраторам для управления всеми пользователями.
    Обычные пользователи могут работать со своим профилем через /users/me/.
    """
    serializer_class = UserSerializer
    lookup_field = 'username'
    http_method_names = ('get', 'patch', 'delete')
    permission_classes = (IsAdminUser,)
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_class = UserFilter
    search_fields = ('username', 'email')

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

    @user_get_schema
    @user_patch_schema
    @user_delete_schema
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


@extend_schema_view(
    list=order_list_schema,
    create=order_create_schema,
    retrieve=order_detail_schema,
    partial_update=order_patch_schema,
    destroy=order_delete_schema,
)
class OrderViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления заказами.
    Аутентифицированные пользователи видят только свои заказы.
    Администраторы видят все заказы и дополнительную информацию.
    """
    queryset = Order.objects.none()
    http_method_names = ('get', 'post', 'patch', 'delete')
    permission_classes = (IsOrdererOrAdmin,)
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_class = OrderFilter
    search_fields = ('title', 'description')

    def get_queryset(self):
        """Возвращает заказы в зависимости от прав пользователя."""
        orders = Order.objects.select_related('user')
        return (orders if self.request.user.is_staff
                else orders.filter(user=self.request.user))

    def filter_queryset(self, queryset):
        """
        Применяет фильтрацию и поиск к queryset.
        Для администраторов доступны все фильтры и поиск.
        Для обычных пользователей доступен только поиск.
        """
        if self.request.user.is_staff:
            return super().filter_queryset(queryset)
        else:
            return SearchFilter().filter_queryset(self.request, queryset, self)

    def get_serializer_class(self):
        """Возвращает подходящий сериализатор в зависимости от пользователя."""
        if self.request.user.is_staff and self.action != 'create':
            return OrderSerializer
        return OrderShortSerializer

    def perform_create(self, serializer):
        """Автоматически привязывает заказ к текущему пользователю."""
        serializer.save(user=self.request.user)
