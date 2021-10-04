from django.contrib import admin

# Import Music model
from .models import User

# Register Music model
admin.site.register(User)