import sys
from flask import Flask
from flask.ext import login
from flask.ext.mongoengine import MongoEngine, MongoEngineSessionInterface
from flask_bootstrap import Bootstrap

neobug = Flask(__name__)
Bootstrap(neobug)
if 'neobug.test.config' in sys.modules:
    neobug.config.from_object(sys.modules['neobug.test.config'])
else:
    neobug.config['MONGODB_SETTINGS'] = {'DB': 'neobug'}
    neobug.config['SECRET_KEY'] = 'KupiKotaZaStoBaksov'

db = MongoEngine(neobug)
neobug.session_interface = MongoEngineSessionInterface(db)
from neobug.models import User
from neobug import views


def init_login():
    login_manager = login.LoginManager()
    login_manager.init_app(neobug)

    @login_manager.user_loader
    def load_user(user_id):
        return User.objects.where("this.username=='" + user_id + "'")[0]

init_login()

if __name__ == "__main__":
    neobug.run()
