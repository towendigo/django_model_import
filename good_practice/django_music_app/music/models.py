from django.db import models

# -------------------------------------------------------
# Music has id, name and artists (Music can be produced by many artists)
# -------------------------------------------------------


# Music need artists but we do not need to import Users as a class:


# Music model
# -------------------------------------------------------
class Music(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200)

    # String represantations work for foreign models so just use that
    # We are going to learn why but :  
    # The part before . is app's name. And after . it is model's name. 
    # So use it like <app's name>.<model's name>
    artists = models.ManyToManyField('user.User') 

    # ------ nicname model -------- 
    def __str__(self) -> str:
        return '%s by %s' %(self.name, " and ".join(self.artists.name) )
    # ----------------------------- 
# -------------------------------------------------------