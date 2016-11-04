from api.models import Album, Image
from api.auth import ImageIsOwnerOrReadOnly, AlbumIsOwnerOrReadOnly
from django.db.models import Q
from api.serializers import (
    UserSignUpSerializer,
    UserSignInSerializer,
    AlbumSerializer,
    AlbumCreateSerializer,
    ImageSerializer,
)
from django.contrib.auth.models import User
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticatedOrReadOnly,
    IsAdminUser,
)
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import (
    APIView,
)
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.filters import SearchFilter, OrderingFilter


class IndexAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        host = 'http://127.0.0.1:8000/'
        # host = 'http://ec2-52-212-250-18.eu-west-1.compute.amazonaws.com/'
        dic = {
            'api': {
                'auth': {
                    'signin': host+'signin',
                    'signup': host+'signup'
                },
                'album': {
                    'create': host+'api/album/create',
                    'list': host+'api/album',
                    'retrieve': host+'api/album/17',
                },
                'image': {
                    'create': host+'api/image/create',
                    'retrieve': host+'api/image/1',
                }
            }
        }
        return Response(dic)


class UserSignUpAPIView(APIView):
    serializer_class = UserSignUpSerializer
    permission_classes = [AllowAny]
    # queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = UserSignUpSerializer(data=data)
        if serializer.is_valid(raise_exception=False):
            serializer.save()
            new_data = serializer.data
            return Response(new_data, status=HTTP_200_OK)
        result = serializer.errors
        if 'non_field_errors' in result:
            result['msg'] = result['non_field_errors']
        elif 'username' in result:
            result['msg'] = result['username'][0]
        elif 'email' in result:
            result['msg'] = result['email'][0]
        elif 'password' in result:
            result['msg'] = result['password'][0]
        return Response(result, status=HTTP_400_BAD_REQUEST)

class UserSignInAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserSignInSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = UserSignInSerializer(data=data)
        if serializer.is_valid(raise_exception=False):
            new_data = serializer.data
            return Response(new_data, status=HTTP_200_OK)
        result = serializer.errors
        result['msg'] = 'Incorrect email or password'
        return Response(result, status=HTTP_400_BAD_REQUEST)


class AlbumListAPIView(ListAPIView):
    serializer_class = AlbumSerializer
    permission_classes = [AllowAny]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'description', 'users__username']

    def perform_create(self, serializer):
        serializer.save(users=[self.request.user])

    def get_queryset(self, *args, **kwargs):
        query_list = Album.objects.all()
        uid = self.request.GET.get('uid')
        if uid:
            query_list = query_list.filter(
                Q(users__id=uid)
            )
        return query_list


class AlbumCreateAPIView(CreateAPIView):
    serializer_class = AlbumCreateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(users=[self.request.user])


class AlbumRetrieveAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, AlbumIsOwnerOrReadOnly]


class ImageCreateAPIView(CreateAPIView):
    serializer_class = ImageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ImageIsOwnerOrReadOnly]

    # def post(self, request, *args, **kwargs):
    #     data = request.data
    #     serializer = ImageSerializer(data=data)
    #     if serializer.is_valid(raise_exception=False):
    #         serializer.save()
    #         return Response(serializer.data, status=HTTP_200_OK)
    #     result = serializer.errors
    #     if 'non_field_errors' in result:
    #         result['msg'] = result['non_field_errors']
    #     return Response(result, status=HTTP_400_BAD_REQUEST)


class ImageRetrieveAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ImageIsOwnerOrReadOnly]
