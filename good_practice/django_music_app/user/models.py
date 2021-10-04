from django.db import models

# -------------------------------------------------------
# User has id, name and playlists (User can have many playlists)
# Every user need a default playlist when created which can contain their musics 
# -------------------------------------------------------


# User 'really need' playlists so let's import Playlists:
# -------------------------------------------------------
from playlist.models import Playlist
# -------------------------------------------------------


# User model
# -------------------------------------------------------
class User(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200)
  
    # Use string represantations anyway (we need Playlist as a class for save method)
    playlists = models.ManyToManyField('playlist.Playlist', blank=True)

    # ------ nicname model -------- 
    def __str__(self) -> str :
        return '%s' %self.name
    # ----------------------------- 

    def save(self, *args, **kwargs):                
    # This is going to run when we create a user.

        super().save(*args, **kwargs)               
        # Call the "real" save() method before creating a default playlist.
        
        default_playlist = Playlist(name="%s's songs" %self.name)                
        # Create a default playlist
        
        default_playlist.save()                     
        # Save and commit changes

        self.playlists.add(default_playlist)
        # Add default playlist to the user model
# -------------------------------------------------------