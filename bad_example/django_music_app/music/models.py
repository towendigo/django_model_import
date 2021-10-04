from django.db import models

# -------------------------------------------------------
# Music has id, name and artists (Music can be produced by many artists)
# -------------------------------------------------------


# Music need artists so let's import Users:
# -------------------------------------------------------
from user.models import User
# -------------------------------------------------------


# Music model
# -------------------------------------------------------
class Music(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200)
    artists = models.ManyToManyField(User)
# -------------------------------------------------------