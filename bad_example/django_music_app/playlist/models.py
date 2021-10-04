from django.db import models

# -------------------------------------------------------
# Playlist has id, name and musics (Playlists can have many music)
# -------------------------------------------------------


# Playlist need musics so let's import Musics:
# -------------------------------------------------------
from music.models import Music
# -------------------------------------------------------


# Playlist model
# -------------------------------------------------------
class Playlist(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200)
    musics = models.ManyToManyField(Music, blank=True) # A playlist can has 0 music when it's created  
# -------------------------------------------------------