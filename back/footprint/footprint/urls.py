"""footprint URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
from api.views import(
    IndexAPIView,
    UserSignInAPIView,
    UserSignUpAPIView,
    AlbumCreateAPIView,
    AlbumListAPIView,
    AlbumRetrieveAPIView,
    ImageCreateAPIView,
    ImageRetrieveAPIView,
    UserAPIView
)

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^$', IndexAPIView.as_view(), name='index'),
    url(r'^signup/$', UserSignUpAPIView.as_view(), name='signup'),
    url(r'^signin/$', UserSignInAPIView.as_view(), name='signin'),

    url(r'^api/getCurrUser$', UserAPIView.as_view(), name='getCurrUser$'),
    url(r'^api/album/create/$', AlbumCreateAPIView.as_view(), name='album_create'),
    url(r'^api/album/$', AlbumListAPIView.as_view(), name='album_list'),
    url(r'^api/album/(?P<pk>\d+)/$', AlbumRetrieveAPIView.as_view(), name='album_retrieve'),

    url(r'^api/image/create/$', ImageCreateAPIView.as_view(), name='image_create'),
    url(r'^api/image/(?P<pk>\d+)/$', ImageRetrieveAPIView.as_view(), name='image_retrieve'),
    # url(r'^api/', include(router.urls), name='list_album'),

    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^auth/token', obtain_jwt_token),
    url(r'^auth/refresh', refresh_jwt_token),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)