import sys
from flask import Flask
from flask.ext import admin, login
from flask.ext.admin import helpers
from flask.ext.admin.contrib.mongoengine import ModelView
from flask.ext.mongoengine import MongoEngine, MongoEngineSessionInterface


neobug = Flask(__name__)

if 'neobug.test.config' in sys.modules:
    neobug.config.from_object(sys.modules['neobug.test.config'])
else:
    neobug.config['MONGODB_SETTINGS'] = {'DB': 'neobug'}
    neobug.config['SECRET_KEY'] = 'KupiKotaZaStoBaksov'

db = MongoEngine(neobug)
neobug.session_interface = MongoEngineSessionInterface(db)
from neobug.models import *
from neobug.admin_views import *
from neobug import views


from blueprints.wiki.views import wiki
from blueprints.projects.views import projects
neobug.register_blueprint(wiki, url_prefix='/wiki')
neobug.register_blueprint(projects, url_prefix='/projects')


def init_login():
    login_manager = login.LoginManager()
    login_manager.init_app(neobug)

    @login_manager.user_loader
    def load_user(user_id):
        return User.objects.where("this.username=='" + user_id + "'")[0]

init_login()

admin = admin.Admin(neobug, 'neobug', index_view=MyAdminIndexView())
admin.add_view(UserView(User))
admin.add_view(ProjectView(Project))
admin.add_view(IssueView(Issue))
admin.add_view(OverviewView(Overview))

if __name__ == "__main__":
    neobug.run()
