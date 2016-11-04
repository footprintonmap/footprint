from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User)
    age = models.IntegerField()


class Album(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    users = models.ManyToManyField('auth.User', related_name='albums')

    class Meta:
        ordering = ('created',)


class Image(models.Model):
    name = models.CharField(blank=True, max_length=100)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='/images')
    album = models.ForeignKey('Album', related_name='images')
