from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status

from .serializers import (AccessOnlyTokenSerializer, CurrentUserSerializer,
                          OrderShortSerializer, SignUpSerializer,
                          UserSerializer)

TAG_AUTH = 'Аутентификация'
TAG_USERS = 'Управление пользователями'
TAG_PROFILE = 'Пользователь'
TAG_ORDERS = 'Заказы'

bad_request = OpenApiResponse(description='Неверные данные')
unauthorized = OpenApiResponse(description='Необходима авторизация')
forbidden = OpenApiResponse(description='Нет доступа')
not_found = OpenApiResponse(description='Объект не найден')
no_content = OpenApiResponse(description='Успешно удалено')

AUTH_ERRORS = {
    status.HTTP_401_UNAUTHORIZED: unauthorized,
}
VALIDATION_ERRORS = {
    status.HTTP_400_BAD_REQUEST: bad_request,
    status.HTTP_401_UNAUTHORIZED: unauthorized,
}
CRUD_ERRORS = {
    status.HTTP_401_UNAUTHORIZED: unauthorized,
    status.HTTP_404_NOT_FOUND: not_found,
}
FULL_ERRORS = {
    status.HTTP_400_BAD_REQUEST: bad_request,
    status.HTTP_401_UNAUTHORIZED: unauthorized,
    status.HTTP_404_NOT_FOUND: not_found,
}
DELETE_RESPONSES = {
    status.HTTP_204_NO_CONTENT: no_content,
    **CRUD_ERRORS,
}

# Аутентификация
signup_schema = extend_schema(
    tags=[TAG_AUTH],
    summary='Регистрация',
    request=SignUpSerializer,
    responses={
        status.HTTP_201_CREATED: SignUpSerializer,
        **VALIDATION_ERRORS,
    },
    auth=[],
)
token_post_schema = extend_schema(
    tags=[TAG_AUTH],
    summary='Получение токена',
    request=AccessOnlyTokenSerializer,
    responses={
        status.HTTP_200_OK: OpenApiResponse(
            description='Access токен успешно выдан'
        ), **AUTH_ERRORS,
    },
    auth=[],
)

# Пользователи
user_list_schema = extend_schema(
    tags=[TAG_USERS],
    summary='Список пользователей',
    responses={
        status.HTTP_200_OK: UserSerializer(many=True),
        **AUTH_ERRORS,
    },
)
user_retrieve_schema = extend_schema(
    tags=[TAG_USERS],
    summary='Получение пользователя',
    responses={
        status.HTTP_200_OK: UserSerializer,
        **CRUD_ERRORS,
    },
)
user_partial_update_schema = extend_schema(
    tags=[TAG_USERS],
    summary='Частичное обновление пользователя',
    request=UserSerializer,
    responses={
        status.HTTP_200_OK: UserSerializer,
        **FULL_ERRORS,
    },
)
user_destroy_schema = extend_schema(
    tags=[TAG_USERS],
    summary='Удаление пользователя',
    responses=DELETE_RESPONSES,
)

# Текущий пользователь
user_get_schema = extend_schema(
    tags=[TAG_PROFILE],
    summary='Получить данные',
    responses={
        status.HTTP_200_OK: CurrentUserSerializer,
        **AUTH_ERRORS,
    },
    methods=['GET'],
)
user_patch_schema = extend_schema(
    tags=[TAG_PROFILE],
    summary='Обновить данные',
    request=CurrentUserSerializer,
    responses={
        status.HTTP_200_OK: CurrentUserSerializer,
        **VALIDATION_ERRORS,
    },
    methods=['PATCH'],
)
user_delete_schema = extend_schema(
    tags=[TAG_PROFILE],
    summary='Удалить аккаунт',
    responses={
        status.HTTP_204_NO_CONTENT: no_content,
        **AUTH_ERRORS,
    },
    methods=['DELETE'],
)

# Заказы
order_list_schema = extend_schema(
    tags=[TAG_ORDERS],
    summary='Список заказов',
    responses={
        status.HTTP_200_OK: OrderShortSerializer(many=True),
        **AUTH_ERRORS,
    },
)
order_create_schema = extend_schema(
    tags=[TAG_ORDERS],
    summary='Создание заказа',
    request=OrderShortSerializer,
    responses={
        status.HTTP_201_CREATED: OrderShortSerializer,
        **VALIDATION_ERRORS,
    },
)
order_detail_schema = extend_schema(
    tags=[TAG_ORDERS],
    summary='Детали заказа',
    responses={
        status.HTTP_200_OK: OrderShortSerializer,
        **CRUD_ERRORS,
    },
)
order_patch_schema = extend_schema(
    tags=[TAG_ORDERS],
    summary='Обновить заказ',
    request=OrderShortSerializer,
    responses={
        status.HTTP_200_OK: OrderShortSerializer,
        **FULL_ERRORS,
    },
    methods=['PATCH'],
)
order_delete_schema = extend_schema(
    tags=[TAG_ORDERS],
    summary='Удалить заказ',
    responses=DELETE_RESPONSES,
    methods=['DELETE'],
)
