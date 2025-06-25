from django.conf import settings
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from orders.models import Order, User


class BaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'birth_date')

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        return {key: value for key, value in rep.items() if value is not None}


class UserSerializer(BaseUserSerializer):
    age = serializers.IntegerField(read_only=True)

    class Meta(BaseUserSerializer.Meta):
        fields = ('id', *BaseUserSerializer.Meta.fields, 'age')


class CurrentUserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = BaseUserSerializer.Meta.fields


class SignUpSerializer(BaseUserSerializer):
    password = serializers.CharField(
        write_only=True, min_length=settings.PASSWORD_MIN_LENGTH)

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
    def validate(self, attrs):
        data = super().validate(attrs)
        data.pop('refresh', None)
        return data


class OrderShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'title', 'description', 'created_at')


class OrderSerializer(OrderShortSerializer):
    user = serializers.SlugRelatedField(read_only=True, slug_field='username')

    class Meta(OrderShortSerializer.Meta):
        fields = (*OrderShortSerializer.Meta.fields, 'updated_at', 'user')
