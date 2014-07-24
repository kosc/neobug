from flask.ext import login, admin
from flask.ext.admin.contrib.mongoengine import ModelView
from neobug.models import Bug

class MyBaseModelView(ModelView):
    def is_accessible(self):
        return login.current_user.is_admin()

class MyAdminIndexView(admin.AdminIndexView):
    def is_accessible(self):
        return login.current_user.is_admin()

class ProjectView(MyBaseModelView):
    form_subdocuments = Bug()
