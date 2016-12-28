from rest_framework_jwt.settings import api_settings
from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.serializers import ImageField
# from datetime import datetime


def get_token(my_user):
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

    payload = jwt_payload_handler(my_user)

    # Include original issued at time for a brand new token,
    # to allow token refresh
    # if api_settings.JWT_ALLOW_REFRESH:
    #     payload['orig_iat'] = timegm(
    #         datetime.utcnow().utctimetuple()
    #     )

    return {
        'token': jwt_encode_handler(payload)
    }


class ImageIsOwnerOrReadOnly(BasePermission):
    message = 'You must be the owner of this object'

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user in obj.album.users.all()


class AlbumIsOwnerOrReadOnly(BasePermission):
    message = 'You must be the owner of this object'

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user in obj.users.all()

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
        print("aaaaaaa")
        # Check if this is a base64 string
        if isinstance(data, six.string_types):
            print("bbbb")
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