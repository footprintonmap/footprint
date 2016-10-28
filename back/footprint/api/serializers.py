from rest_framework.serializers import (
    ModelSerializer,
    PrimaryKeyRelatedField,
    CharField,
    EmailField,
    ValidationError,
)
from .models import *
from django.db.models import Q
from api.auth import get_token


class UserSignUpSerializer(ModelSerializer):
    token = CharField(allow_blank=True, read_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'token')
        extra_kwargs = {
            "password": {
                "write_only": True
            }
        }

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']
        user_obj = User(
            username=username,
            email=email,
        )
        user_obj.set_password(password)
        user_obj.save()
        validated_data['token'] = get_token(user_obj)['token']
        return validated_data

    def validate(self, data):
        email = data['email']
        password = data['password']
        if User.objects.filter(email=email).exists():
            raise ValidationError('This email is already registered.')
        if len(password) < 6:
            raise ValidationError('Your password must be at least 6 characters.')
        return data


class UserSignInSerializer(ModelSerializer):
    token = CharField(allow_blank=True, read_only=True)
    email = EmailField(label='Email Address')

    class Meta:
        model = User
        fields = ['email', 'password', 'token']
        extra_kwargs = {
            "password": {
                "write_only": True
            }
        }

    def validate(self, data):
        email = data['email']
        password = data['password']
        user = User.objects.filter(Q(email=email)).distinct()
        if user.exists():
            user_obj = user.first()
        else:
            raise ValidationError('This email is not valid.')
        if user_obj:
            if not user_obj.check_password(password):
                raise ValidationError('Incorrect password, please try again.')

        data['token'] = get_token(user_obj)['token']
        return data


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')


class ImageSerializer(ModelSerializer):
    class Meta:
        model = Image
        field = ('name', 'description', 'image')


class AlbumSerializer(ModelSerializer):
    users = UserSerializer(many=True, read_only=True)
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Album
        fields = ('id', 'name', 'description', 'created', 'modified', 'users', 'images')


class AlbumCreateSerializer(ModelSerializer):
    users = PrimaryKeyRelatedField(many=True, read_only=True)
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Album
        fields = ('id', 'name', 'description', 'created', 'modified', 'users', 'images')
