from django.conf import settings
from django.contrib.auth import get_user_model
from orders.models import Order
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class BaseUserSerializer(serializers.ModelSerializer):
    """
    Базовый сериализатор для пользователя.
    Автоматически исключает поля со значением None из ответа.
    """
    class Meta:
        model = User
        fields = ('username', 'email', 'birth_date')

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        return {key: value for key, value in rep.items() if value is not None}


class UserSerializer(BaseUserSerializer):
    """
    Сериализатор пользователя для административных функций.
    Включает автоматически вычисляемое поле возраста.
    """
    age = serializers.IntegerField(
        read_only=True,
        help_text='Автоматически вычисляется на основе даты рождения'
    )

    class Meta(BaseUserSerializer.Meta):
        fields = ('id', *BaseUserSerializer.Meta.fields, 'age')


class CurrentUserSerializer(BaseUserSerializer):
    """
    Сериализатор для работы с профилем текущего пользователя.
    Позволяет получать и обновлять данные профиля.
    """
    class Meta(BaseUserSerializer.Meta):
        fields = BaseUserSerializer.Meta.fields


class SignUpSerializer(BaseUserSerializer):
    """
    Сериализатор для регистрации нового пользователя.
    Включает валидацию пароля и создание нового пользователя.
    """
    password = serializers.CharField(
        write_only=True,
        min_length=settings.PASSWORD_MIN_LENGTH,
        help_text=f'Минимальная длина: {settings.PASSWORD_MIN_LENGTH} символов'
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'birth_date', 'password')

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class AccessOnlyTokenSerializer(TokenObtainPairSerializer):
    """
    Сериализатор для получения access токена.
    Исключает refresh токен из ответа.
    """
    def validate(self, attrs):
        data = super().validate(attrs)
        data.pop('refresh', None)
        return data


class OrderShortSerializer(serializers.ModelSerializer):
    """
    Краткий сериализатор заказа.
    Используется для обычных пользователей, содержит основную информацию.
    """
    class Meta:
        model = Order
        fields = ('id', 'title', 'description', 'created_at')


class OrderSerializer(OrderShortSerializer):
    """
    Полный сериализатор заказа.
    Используется для администраторов, включает дополнительную информацию.
    """
    user = serializers.SlugRelatedField(read_only=True, slug_field='username')

    class Meta(OrderShortSerializer.Meta):
        fields = (*OrderShortSerializer.Meta.fields, 'updated_at', 'user')
