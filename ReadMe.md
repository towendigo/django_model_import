# Django Model Import Loop

The aim of this project is showing what can go wrong when creating models in Django. And teaching some ways to overcome this challenges.

When starting a project, structuring data and logic is essential. In Django we are doing data part with models. And logic part with urls, views, etc... Django models can have logic in them too.

For demonstration we are going to create a music app.

## Music App :
Our app needs musics and playlists obviusly. Musics have artists (users) who produced them. And playlists have musics in them. Users have their playlists too. So we have `Music, Playlist and Artist(User)` models. Also we are going to create a blank playlist for every user to contain musics they produced. 

This might not be the best solution out there for a music app but we are going to do it like that for demonstration purposes.

At the end of the document we are going to try to improve the way we structured our models (data).

## Django Setup : 

---
**I am using cmd most of the time. Ypu should make changes if necessary for your terminal choice !**

I am skipping the python virtual environment part. I just installed django in my python virtual environment.

---

Start a django project named django_music_app with:
```
django-admin startproject django_music_app
```

Then create seperate apps for `Music, Playlist and User` with:
```
::change directory as django app 
cd django_music_app 

::create apps 
python manage.py startapp music 
python manage.py startapp playlist 
python manage.py startapp user 
echo Done...  
cd ..

```

Run makemigrations and migrate commands with:
```
::change directory as django app 
cd django_music_app 

::run commands 
python manage.py makemigrations
python manage.py migrate 
echo Done...  
cd ..

```

Create a super user with:
```
::change directory as django app 
cd django_music_app 

::create superuser
python manage.py createsuperuser

```


In django_music_app/django_music_app/settings.py add `Music, Playlist and User` to installed apps with:
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # add apps
    # ------------------
    'music',
    'user',
    'playlist',
    # ------------------
]
```

## Django Models (Bad Example):

### Music :

In django_music_app/music/models.py create a music model with :
```python
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
```

Register model in django_music_app/music/admin.py with:
```python
from django.contrib import admin

# Import Music model
from .models import Music

# Register Music model
admin.site.register(Music)
```

### Playlist :

In django_music_app/playlist/models.py create a playlist model with :
```python
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
```

Register model in django_music_app/playlist/admin.py with:
```python
from django.contrib import admin

# Import Music model
from .models import Playlist

# Register Music model
admin.site.register(Playlist)
```

### User :

In django_music_app/user/models.py create a user model with :

```python
from django.db import models

# -------------------------------------------------------
# User has id, name and playlists (User can have many playlists)
# Every user need a default playlist when created which can contain their musics 
# -------------------------------------------------------


# User need playlists so let's import Playlists:
# -------------------------------------------------------
from playlist.models import Playlist
# -------------------------------------------------------


# User model
# -------------------------------------------------------
class User(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200)
    playlists = models.ManyToManyField(Playlist , blank=True))

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
```

Register model in django_music_app/user/admin.py with:
```python
from django.contrib import admin

# Import Music model
from .models import User

# Register Music model
admin.site.register(User)
```

### Migrations :

Run makemigrations and migrate commands again with:
```
::run commands 
python manage.py makemigrations
python manage.py migrate 
echo Done...  
cd ..

```

There should be an error. Read bad_example/Error.MD for further information (I highly recommend reading it). 
You can find this version in bad_example/django_music_app.

I am going to show you how to solve this problem. I am going to show you an overkill method (django built-in model imports) too.

## Refactoring Models (Good Practice):

Django is a highly opinionated framework. Which means Django usually has a way to handle things and has an opinion of how you should handle things. This makes it robust and fast for development. Ideally we want django to handle things as much as possible. So let's make our models more Django-ish and let Django handle foreign models.

### Music :

In django_music_app/music/models.py change music model as :

```python
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
# -------------------------------------------------------
```

### Playlist :

In django_music_app/playlist/models.py change playlist model as :

```python
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
    musics = models.ManyToManyField('music.Music', null=True, blank=True)
# -------------------------------------------------------
```

#### User :

In django_music_app/user/models.py change user model as :

```python
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

    def save(self, *args, **kwargs):                
    # This is going to run when we create a user.

        super().save(*args, **kwargs)               
        # Call the "real" save() method
        
        default_playlist = Playlist(name="%s's songs" %self.name)                
        # Create a default playlist
        
        default_playlist.save()                     
        # Save and commit changes

        self.playlists.add(default_playlist)
        # Add default playlist to the user model
# -------------------------------------------------------
```

### Migrations :

Run makemigrations and migrate commands again with:
```
::run commands 
python manage.py makemigrations
python manage.py migrate 
echo Done...  
cd ..

```

It should be successful now. We solved recursive import problem with using string represantations if possible.

### Making Models Human Readable :

In Django, models have a method named `__str__`. This method returns a nick-name for model thus make it human readable.

I am going to add user and playlist models (class) this code (method) :
```python
    # ------ nicname model -------- 
    def __str__(self) -> str :
        return '%s' %self.name
    # ----------------------------- 
```

And add music model (class) this code (method) :

```python
    # ------ nicname model -------- 
    def __str__(self) -> str:
        return '%s by %s' %(self.name, " and ".join(self.artists.name) )
    # ----------------------------- 
```

### Trying Models :

Run Django development server with :
```
::run server 
python manage.py runserver

```

You should get an output like that:
```
Django version 3.2.7, using settings 'django_music_app.settings'
Starting development server at http://0.0.0.0:8000/
Quit the server with CTRL-BREAK.

```

http: //0.0.0.0 part can be different but we can just use localhost instead. So http: //0.0.0.0:8000/ is same with localhost:8000. 

Find which port (:8000 part) django uses. And than visit localhost:port/admin (for example localhost:8000/admin) on your browser. Log in as the superuser you have created. Try to add and change and delete models.

You can find complete code in good_practice/django_music_app but i deleted db and migrations so it might not work if you try to run it. 

I highly recommend doing everything in a single django project as i did and using bad_example - good_practice folders for just looking at the code if needed.


## Django Model Loaders (django_model_loaders -overkill-):