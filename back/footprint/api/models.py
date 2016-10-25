from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User)
    age = models.IntegerField()


class Album(models.Model):
    name = models.CharField(max_length=100, blank=True, default='')
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    users = models.ManyToManyField('auth.User',related_name='albums')
    

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('created',)


class Image(models.Model):
    name = models.CharField(max_length=100, blank=True, default='')
    image = models.ImageField()

    album = models.ForeignKey('Album')