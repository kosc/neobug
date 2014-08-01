from wtforms.fields import SelectField
from flask.ext import login, admin
from flask.ext.admin.form import rules
from flask.ext.admin.contrib.mongoengine import ModelView

from neobug.models import Issue, Project


class MyBaseModelView(ModelView):

    def is_accessible(self):
        return login.current_user.is_admin()


class MyAdminIndexView(admin.AdminIndexView):

    def is_accessible(self):
        return login.current_user.is_admin()


class UserView(MyBaseModelView):
    column_list = ('username', 'email')


class ProjectView(MyBaseModelView):
    pass


class IssueView(ModelView):
    form_overrides = dict(status=SelectField, category=SelectField)
    form_args = dict(
        status=dict(
            choices=zip(Issue.statuses, Issue.statuses)
        ),
        category=dict(
            choices=zip(Issue.categories, Issue.categories)
        )
    )
    form_subdocuments = {
        'comments': {
            'form_subdocuments': {
                None: {
                    'form_rules': ('body', 'author', rules.HTML('<hr>'))
                }
            }
        }
    }
