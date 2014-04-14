from flask.ext.mongoengine.wtf import model_form
from wtforms.fields import *
from neobug.models import *


UserForm = model_form(User, exclude=['password_hash', 'password_salt'])
ProjectForm = model_form(Project, exclude=['created_at', 'bugs'])
BugForm = model_form(Bug, exclude=['created_at', 'comments', 'author'])
CommentForm = model_form(Comment, exclude=['created_at', 'author'])


class RegisterForm(UserForm):
    password = PasswordField('Password')
    repeat = PasswordField('Repeat password')


class LoginForm(UserForm):
    password = PasswordField('Password')
