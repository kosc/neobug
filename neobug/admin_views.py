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
    form_excluded_columns = ('password_hash', 'password_salt')


class ProjectView(MyBaseModelView):
    pass


class IssueView(ModelView):
    projects_ids = Project.objects.distinct("id")
    projects_ids = [str(project_id) for project_id in projects_ids]
    projects_names = Project.objects.distinct("name")
    form_overrides = dict(status=SelectField,
                          category=SelectField,
                          project_id=SelectField)
    form_args = dict(
        status=dict(
            choices=zip(Issue.statuses, Issue.statuses)
        ),
        category=dict(
            choices=zip(Issue.categories, Issue.categories)
        ),
        project_id=dict(
            choices=zip(projects_ids, projects_names)
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
