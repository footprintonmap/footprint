from rest_framework_jwt.settings import api_settings
from rest_framework.permissions import BasePermission, SAFE_METHODS
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
