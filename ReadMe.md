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

In Django you can load apps and models with built-in modules. Django itself does that actually.

---
Model loaders in this case works for Django 3+ (Specifically Django==3.2.7). I did not check for other versions. If you want to do that feel free to contact me. I am planning to do an automated test but not right now.

You should be able to follow this guide as long as you can find the code examples below in your Django distribution. 

---

### How Django Does That :

In Django distribution there is a folder called apps. In that folder there is `config.py` , `registry.py`, `__init__.py` and other files (`__pycache__` folder) related to the apps module.

`__init__.py` file looks like that: 

```python
from .config import AppConfig
from .registry import apps

__all__ = ['AppConfig', 'apps']
```

`config.py` file has a class called `AppConfig` for representing a Django application and it's configurations. 

This class has a method for returning models based on model names.

```python
# ... (This means there is cods that i do not show because they have nothing to do for what we are looking in this case)

class AppConfig:
    """Class representing a Django application and its configuration."""

    # ...

    def get_model(self, model_name, require_ready=True):
        """
        Return the model with the given case-insensitive model_name.

        Raise LookupError if no model exists with this name.
        """
        if require_ready:
            self.apps.check_models_ready()
        else:
            self.apps.check_apps_ready()
        try:
            return self.models[model_name.lower()]
        except KeyError:
            raise LookupError(
                "App '%s' doesn't have a '%s' model." % (self.label, model_name))

    # ...
```

`registry.py` file has a class called `Apps` for storing the configuration of installed applications and keeping track of models, e.g. to provide reverse relations. 

This class has a method for:
*   Returning apps based on app names 
*   Returning models based on app names and model names
*   Returning models based on app names and model names (safer)

```python
# ...

from .config import AppConfig

class Apps:
    """
    A registry that stores the configuration of installed applications.

    It also keeps track of models, e.g. to provide reverse relations.
    """
    
    # ...

    def get_app_config(self, app_label):
        """
        Import applications and returns an app config for the given label.

        Raise LookupError if no application exists with this label.
        """
        self.check_apps_ready()
        try:
            return self.app_configs[app_label]
        except KeyError:
            message = "No installed app with label '%s'." % app_label
            for app_config in self.get_app_configs():
                if app_config.name == app_label:
                    message += " Did you mean '%s'?" % app_config.label
                    break
            raise LookupError(message)

    # ...
    
    def get_model(self, app_label, model_name=None, require_ready=True):
        """
        Return the model matching the given app_label and model_name.

        As a shortcut, app_label may be in the form <app_label>.<model_name>.

        model_name is case-insensitive.

        Raise LookupError if no application exists with this label, or no
        model exists with this name in the application. Raise ValueError if
        called with a single argument that doesn't contain exactly one dot.
        """
        if require_ready:
            self.check_models_ready()
        else:
            self.check_apps_ready()

        if model_name is None:
            app_label, model_name = app_label.split('.')

        app_config = self.get_app_config(app_label)

        if not require_ready and app_config.models is None:
            app_config.import_models()

        return app_config.get_model(model_name, require_ready=require_ready)

    # ...

    def get_registered_model(self, app_label, model_name):
        """
        Similar to get_model(), but doesn't require that an app exists with
        the given app_label.

        It's safe to call this method at import time, even while the registry
        is being populated.
        """
        model = self.all_models[app_label].get(model_name.lower())
        if model is None:
            raise LookupError(
                "Model '%s.%s' not registered." % (app_label, model_name))
        return model

    # ...

apps = Apps(installed_apps=None)
```

---
```python
def get_model(self, app_label, model_name=None, require_ready=True):
        """
        Return the model matching the given app_label and model_name.

        As a shortcut, app_label may be in the form <app_label>.<model_name>.

        model_name is case-insensitive.
        ...
        """
```
This is why we use `<app's name>.<model's name>` in models as string represantations.

---

This is how django does it.

### How We Can Use That :

In a django file like urls, views and models we can import that method and use it directly. Or we can create a model loader module and use that instead. Creating a model loader gives us more flexibility.

#### Direct Use :

Let's use our models. We are going to change user model. But i am not going to add this into repository.

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
# ... (rest is same)


#-#-#-#-#-# as #-#-#-#-#-#


from django.db import models

# from django.apps import apps class as AppLoader and then use get_model method
# -------------------------------------------------------
from django.apps import apps as AppLoader
# -------------------------------------------------------

# -------------------------------------------------------
# User has id, name and playlists (User can have many playlists)
# Every user need a default playlist when created which can contain their musics 
# -------------------------------------------------------


# User 'really need' playlists so let's get it with get_model instead of importing:
# -------------------------------------------------------
Playlist = AppLoader.get_model(app_label="playlist.Playlist", require_ready=False)
# -------------------------------------------------------
# ... (rest is same)
```

#### Indirect Use :

In django_music_app/django_music_app folder create a file called `model_loader.py`.

`model_loader.py` : 
```python
from django.apps import apps as AppLoader

def Single_Loader(app_name, model_name = False, strict= False):
    try :
        return AppLoader.get_model(app_name, model_name, strict)
    except :
        return None
        # You can do something if there is an error


def Multi_Loader(app_name, model_names : list, strict= False):
    try : 
        return_models = []   # You can pass model names as list and get a model object list 
        for model_name in model_names:
            return_models.append(AppLoader.get_model(app_name, model_name, strict))
        return return_models
    except :
        return None
```

Etc...

You can import this methods like:

```python
from project_name.model_loader import Multi_Loader
``` 

Let's use our models. We are going to change user model. But i am not going to add this into repository.

```python
from django.db import models

# Import custom model loaders
from django_music_app.model_loader import Single_Loader

# -------------------------------------------------------
# User has id, name and playlists (User can have many playlists)
# Every user need a default playlist when created which can contain their musics 
# -------------------------------------------------------


# User 'really need' playlists so let's use custom model loader for Playlists:
# -------------------------------------------------------
Playlist = Single_Loader(app_name='playlist', model_name = 'Playlist', strict= False)
# -------------------------------------------------------
# ... (rest is same)
```

Instead of `apps.get_model()` you can load models like this if needed:

```python
from django.apps import apps as AppLoader

def Single_Loader(app_name, model_name, err_code=False):
    try:
        App = AppLoader.get_app_config(app_name) 
        # get app first 
        
        return App.get_model(model_name) 
        # get model with app.get_model(model_name) instead of apps.get_model(app_name, model_name)

        # This can be beneficial if you need more than one model 
        # from same app since this method loads app once and use 
        # it as many times as you want
    except:
        return None
```


## END

Author : Akif Sahin Korkmaz
