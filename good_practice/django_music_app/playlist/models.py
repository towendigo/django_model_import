from django.db import models

# -------------------------------------------------------
# Playlist has id, name and musics (Playlists can have many music)
# -------------------------------------------------------


# Playlist need musics but we do not need to import Musics


# Playlist model
# -------------------------------------------------------
class Playlist(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200)
    musics = models.ManyToManyField('music.Music', blank=True)

    # ------ nicname model -------- 
    def __str__(self) -> str :
        return '%s' %self.name
    # ----------------------------- 
# -------------------------------------------------------