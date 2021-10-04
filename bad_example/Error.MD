## Looks like we have an error.
---

Error:
```
  File "...\django_music_app\music\models.py", line 10, in <module>
    from user.models import User

  File "...\django_music_app\user\models.py", line 11, in <module>
    from playlist.models import Playlist

  File "...\django_music_app\playlist\models.py", line 10, in <module>
    from music.models import Music

ImportError: cannot import name 'Music' from 'music.models' (...\django_music_app\music\models.py)
```


The reason behind this error is this:

```
1. Music model imports User model
2. User model imports Playlist model
3. Playlist model imports Music model
              
                 ||
                _||_
                \  /
                 \/

4. Music model imports User model
5. User model imports Playlist model
6. Playlist model imports Music model

                 ||
                _||_
                \  /
                 \/

4. Music model imports User model
5. ...
6. ...
.
.
.
```


Did you spot what happend? We have created a recursive import loop to the infinity. In real world it just crashes the app because we are trying to import something that is not there yet because it is trying to import something that is not there yet because...

