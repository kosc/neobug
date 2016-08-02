from flask_mongoengine.wtf import model_form
from wtforms.fields import *
from neobug.models import *


UserForm = model_form(User, exclude=['password_hash', 'password_salt'])


class RegisterForm(UserForm):
    password = PasswordField('Password')
    repeat = PasswordField('Repeat password')


class LoginForm(UserForm):
    password = PasswordField('Password')
