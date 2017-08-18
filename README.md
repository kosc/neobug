neobug
======

Light bugtracker system on flask and mongodb. Your can see demo site at [http://neobug.hotkosc.ru](http://neobug.hotkosc.ru)

TODO:
-----
* Add AJAX for forms
* Typography (FIXME, TODO, WARNING, INFO, etc)
* Cut (Spoiler)
* Sidebar
* Git hosting (with forks and pullrequests)

DEPENDENCIES:
-------------
* lxml (for testing)
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

1. Clone repo with "git clone https://github.com/kosc/neobug.git"
2. Install all dependencies (python dependencies can be install from requirements.txt with pip)
3. Create a `neobug/local_settings.py` by this example:
```
DB_HOSTNAME = 'db' # Your database host, 127.0.0.1 if db running on same server
DB_NAME = 'neobug'

SECRET_KEY = 'ZaikaDropnulTable'
```
4. Run ./manage.py debug for debug and ./manage.py runserver for common using.
5. Register your account on http://localhost:5000/.
6. Make your user administrator:
  Run ./manage.py shell and run:
  
```python
from neobug.models import User
user = User.objects(username="login")[0] # where login is your user's username from step 4.
user.admin = True
user.save()
```
