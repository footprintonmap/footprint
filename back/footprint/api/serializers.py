from rest_framework.serializers import (
    ModelSerializer,
    PrimaryKeyRelatedField,
    CharField,
    EmailField,
    ValidationError,
    SerializerMethodField,
    ImageField
)
from .models import *
from django.db.models import Q
from api.auth import get_token

class Base64ImageField(ImageField):
    """
    A Django REST framework field for handling image-uploads through raw post data.
    It uses base64 for encoding and decoding the contents of the file.

    Heavily based on
    https://github.com/tomchristie/django-rest-framework/pull/1268

    Updated for Django REST framework 3.
    """

    def to_internal_value(self, data):
        from django.core.files.base import ContentFile
        import base64
        import six
        import uuid

        # Check if this is a base64 string
        if isinstance(data, six.string_types):
            # Check if the base64 string is in the "data:" format
            if 'data:' in data and ';base64,' in data:
                # Break out the header from the base64 content
                header, data = data.split(';base64,')

            # Try to decode the file. Return validation error if it fails.
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            # Generate file name:
            file_name = str(uuid.uuid4())[:12] # 12 characters are more than enough.
            # Get the file name extension:
            file_extension = self.get_file_extension(file_name, decoded_file)

            complete_file_name = "%s.%s" % (file_name, file_extension, )

            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension

class UserSignUpSerializer(ModelSerializer):
    token = CharField(allow_blank=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'token')
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
        fields = ['id', 'username', 'email', 'password', 'token']
        extra_kwargs = {
            "password": {
                "write_only": True
            },
            "username": {
                "read_only": True
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
        data['username'] = user_obj.username
        data['id'] = user_obj.id
        return data


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')


class ImageSerializer(ModelSerializer):
    image = Base64ImageField(max_length=None, use_url=True)
    class Meta:
        model = Image
        fields = ('name', 'description', 'image', 'album')

    def create(self, validated_data):
        name = validated_data['name']
        description = validated_data['description']
        image = validated_data['image']

        album = validated_data['album']
        image_obj = Image(
            name=name,
            description=description,
            image=image,
            album=album
        )
        image_obj.save()
        return image_obj

    def validate(self, data):
        album = data['album']
        if not self.context['request'].user in album.users.all():
            raise ValidationError('You are not the owner')
        return data


class GeoSerializer(ModelSerializer):

    class Meta:
        model = Geo
        fields = ('id', 'name', 'lat', 'lng')


class AlbumSerializer(ModelSerializer):
    users = UserSerializer(many=True, read_only=True)
    images = ImageSerializer(many=True, read_only=True)
    geo = GeoSerializer(many=False, read_only=True)

    class Meta:
        model = Album
        fields = ('id', 'name', 'description', 'created', 'modified', 'users', 'images', 'geo')


class AlbumCreateSerializer(ModelSerializer):
    users = PrimaryKeyRelatedField(many=True, read_only=True)
    images = ImageSerializer(many=True, read_only=True)
    geo = GeoSerializer(many=False)

    class Meta:
        model = Album
        fields = ('id', 'name', 'description', 'created', 'modified', 'users', 'images', 'geo')

    def create(self, validated_data):
        geo = validated_data['geo']

        geo_obj = Geo(
            name=geo['name'],
            lat=geo['lat'],
            lng=geo['lng']
        )
        geo_obj.save()
        validated_data.pop('geo')
        validated_data['geo']=geo_obj

        return super(AlbumCreateSerializer, self).create(validated_data)


