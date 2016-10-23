from django.contrib.auth.models import User, Group
from rest_framework import viewsets

from rest_framework import generics
from api.models import Album
from api.serializers import UserSerializer, GroupSerializer, AlbumSerializer
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route
from rest_framework.pagination import PageNumberPagination
from rest_framework import permissions

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class AlbumViewSet(viewsets.ModelViewSet):
    # class page(PageNumberPagination):
    #     page_size = 5
    #     page_size_query_param = 'page'
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    # pagination_class = page

    def perform_create(self, serializer):
        serializer.save(users=[self.request.user])