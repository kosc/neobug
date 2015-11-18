neobug
======

Light bugtracker system on flask and mongodb.

TODO:
-----
* Add AJAX for forms
* Typography (FIXME, TODO, WARNING, INFO, etc)
* Cut (Spoiler)
* Sidebar
* Git hosting (with forks and pullrequests)

DEPENDENCIES:
-------------
* MongoDB >= 3.0.7
* Flask>=0.10.1
  * Flask-Login>=0.2.11
  * Flask-WTF>=0.10.0
  * Flask-Admin>=1.0.8
  * Flask-Script>=2.0.5
  * flask-mongoengine>=0.7.0
* python >= 3.3

INSTALLATION MANUAL:
--------------------

1. Install all dependencies (python dependencies can be install from requirements.txt with pip)
2. Clone repo with "git clone https://github.com/kosc/neobug.git"
3. Run ./manage.py debug for debug and ./manage.py runserver for common using.
4. Register your account on http://localhost:5000/.
5. Make your user administrator:
  Run ./manage.py shell and run:
  
```python
from neobug.models import User
user = User.objects(username=login)[0] # where login is your user's username from step 4.
user.is_admin = True
user.save()
```
