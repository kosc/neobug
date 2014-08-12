from flask.ext.mongoengine.wtf import model_form
from wtforms.fields import *
from neobug.models import *


UserForm = model_form(User, exclude=['password_hash', 'password_salt'])
ProjectForm = model_form(Project, exclude=['created_at', 'bugs'])
IssueForm = model_form(Issue, exclude=['created_at',
                                       'comments',
                                       'author',
                                       'status',
                                       'category'])
CommentForm = model_form(Comment, exclude=['created_at', 'author'])


class RegisterForm(UserForm):
    password = PasswordField('Password')
    repeat = PasswordField('Repeat password')


class LoginForm(UserForm):
    password = PasswordField('Password')
