from django.contrib import admin

# Import Music model
from .models import Music

# Register Music model
admin.site.register(Music)