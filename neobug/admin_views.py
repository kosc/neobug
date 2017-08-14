from wtforms.fields import SelectField
import flask_admin
import flask_login
from flask_admin.form import rules
from flask_admin.contrib.mongoengine import ModelView

from neobug.models import Issue, Project


class MyBaseModelView(ModelView):

    def is_accessible(self):
        return flask_login.current_user.is_admin()


class MyAdminIndexView(flask_admin.AdminIndexView):

    def is_accessible(self):
        return flask_login.current_user.is_admin()


class UserView(MyBaseModelView):
    column_list = ('username', 'email', 'admin')
    form_excluded_columns = ('password_hash', 'password_salt')


class DownloadView(MyBaseModelView):
    pass


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
            'form_columns': ('body', 'author', rules.HTML('<hr>'))
        }
    }


class OverviewView(MyBaseModelView):
    pass
