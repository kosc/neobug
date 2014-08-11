from flask.ext.mongoengine.wtf import model_form
from wtforms.fields import *
from neobug.models import Project, Issue, Comment

IssueForm = model_form(Issue, exclude=['created_at', 'comments', 'author', 'status', 'category'])
ProjectForm = model_form(Project, exclude=['created_at'])
CommentForm = model_form(Comment, exclude=['created_at', 'author'])
