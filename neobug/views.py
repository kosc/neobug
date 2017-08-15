from hashlib import sha512
from uuid import uuid4

from flask import (render_template, request, url_for,
                   redirect, session, g)
from flask_login import login_user, logout_user

from neobug.models import *
from neobug import forms
from neobug import neobug


@neobug.route('/')
@neobug.route('/index')
def index():
    overview = Overview.objects.first()
    return render_template("index.html",
                           overview=overview)


@neobug.route('/login', methods=('GET', 'POST'))
def login():
    current_page = request.referrer
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode('utf-8')
        user = User.objects(username=username)
        if len(user) == 0:
            return render_template("login.html",
                                   message="Incorrect login")
        user = user[0]
        password_salt = user.password_salt.encode('utf-8')
        password_hash = sha512(password + password_salt).hexdigest()
        if password_hash == user.password_hash:
            session['logged_in'] = True
            g.user = user
            login_user(user)
            return redirect(current_page)
        else:
            return render_template("login.html",
                                   message="Incorrect password")
    return render_template("login.html")


@neobug.route('/logout')
def logout():
    current_page = request.referrer
    logout_user()
    session['logged_in'] = False
    return redirect(current_page)


@neobug.route('/register', methods=('GET', 'POST'))
def register():
    user = User()
    form = forms.RegisterForm(request.form)
    if request.method == 'POST':
        if not form.validate_on_submit():
            message = "This username is already taken."
            return render_template("register.html", message=message, form=form)
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        password_repeat = request.form['repeat']
        if password != password_repeat:
            message = "Password and password repeat must be the same."
            return render_template("register.html", message=message, form=form)
        salt = uuid4().hex
        password_hash = sha512((password + salt).encode('utf-8'))
        user.password_hash = password_hash.hexdigest()
        user.email = email
        user.password_salt = salt
        user.username = username
        user.save()
        session['logged_in'] = True
        g.user = user
        login_user(user)
        return redirect(url_for('index'))
    return render_template("register.html",
                           title="Register",
                           form=form)
