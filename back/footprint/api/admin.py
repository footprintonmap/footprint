from django.contrib import admin
from api.views import *

@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
	list_display = ('id','name','description','created','modified')

# Register your models here.
