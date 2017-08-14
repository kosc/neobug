from flask_mongoengine.wtf import model_form
from wtforms.fields import *
from neobug.models import Project, Issue, Comment

BaseIssueForm = model_form(Issue, exclude=['created_at', 'comments', 'author'])
ProjectForm = model_form(Project, exclude=['created_at'])
CommentForm = model_form(Comment, exclude=['created_at', 'author'])


class IssueForm(BaseIssueForm):
    status = SelectField(choices=list(zip(Issue.statuses, Issue.statuses)))
    category = SelectField(choices=list(zip(Issue.categories, Issue.categories)))
