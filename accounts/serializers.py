from django.contrib.auth import authenticate, password_validation
from django.contrib.sites.models import Site
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.models import User
from django.utils.translation import gettext_lazy as _


class UserAvatarSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField()

    class Meta:
        model = User
        fields = ['avatar']
        read_only_fields = ['id',]


class UserModelSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()

    @extend_schema_field(OpenApiTypes.STR)
    def get_avatar(self, user: User):  # noqa
        if user.avatar:
            return f'{Site.objects.get_current()}{user.avatar.url}'
        return ''

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name', 'email', 'avatar',)


class RegisterSerializer(serializers.ModelSerializer):

    def validate(self, data):
        password = data['password']
        password_validation.validate_password(password)
        data['username'] = User.generate_unique_username(data['email'])
        data['is_active'] = False
        return data

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']


class UserLoginSerializer(serializers.Serializer):  # noqa
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8)

    def validate(self, data):
        user = authenticate(username=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError('Invalid credentials')
        if not user.is_verified:
            raise serializers.ValidationError('Account is not active yet.')
        self.context['user'] = user
        return data

    def create(self, data):
        refresh = RefreshToken.for_user(self.context['user'])
        token = {
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }
        return self.context['user'], token


class UserLogoutSerializer(serializers.Serializer):  # noqa
    user = serializers.CharField()
    auth_user = serializers.CharField()

    def validate(self, data):
        if data['user'] != data['auth_user']:
            raise serializers.ValidationError('Invalid operation')
        user = User.objects.get(username=data['user'])
        self.context['user'] = user
        return data

    def save(self):
        RefreshToken.for_user(self.context['user'])


class ResetPasswordRequestSerializer(serializers.Serializer):  # noqa
    email = serializers.EmailField(required=True)


class ResetPasswordSerializer(serializers.Serializer):  # noqa
    token = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, data):
        token = data.get('token')
        password = data.get('password')
        if not token:
            raise serializers.ValidationError(
                _('El campo "token" es obligatorio.'))
        if not password:
            raise serializers.ValidationError(
                _('El campo "password" es obligatorio.'))
        return data


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):  # noqa
    @classmethod
    def get_token(cls, user):
        token = super(CustomTokenObtainPairSerializer, cls).get_token(user)
        # Add custom claims
        token["user"] = UserModelSerializer(user, many=False).data
        return token


class TokenOutput(serializers.Serializer):  # noqa
    refresh = serializers.CharField(label=_("Refresh token"))
    access = serializers.CharField(label=_("Access token"))


class LogoutSerializer(serializers.Serializer):  # noqa
    refresh_token = serializers.CharField()
