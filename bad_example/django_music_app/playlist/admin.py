from django.contrib import admin

# Import Music model
from .models import Playlist

# Register Music model
admin.site.register(Playlist)
