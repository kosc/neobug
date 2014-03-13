from hashlib import sha512
from uuid import uuid4
from flask import Blueprint, render_template, request, url_for, redirect, session
from flask.ext.login import login_user, logout_user, current_user
from neobug import neobug
from neobug.models import *


@neobug.route('/')
@neobug.route('/index')
def index():
    return render_template("index.html", title="Main page")


@neobug.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode('utf-8')
        user = User.objects.where("this.username=='" + username + "'")
        if len(user) == 0:
            return render_template("login.html", message="Incorrect login")
        user = user[0]
        password_salt = user.password_salt.encode('utf-8')
        password_hash = sha512(password + password_salt).hexdigest()
        if password_hash == user.password_hash:
            session['logged_in'] = True
            login_user(user)
            return redirect('index')
        else:
            return render_template("login.html", message="Incorrect password")
    return render_template("login.html")


@neobug.route('/logout')
def logout():
    logout_user()
    session['logged_in'] = False
    return render_template("index.html")


@neobug.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        password_repeat = request.form['password_repeat']
        if password != password_repeat:
            message = "Password and password repeat must be the same."
            return render_template("register.html", message=message)
        salt = uuid4().hex.encode("utf-8")
        password_hash = sha512(password.encode("utf-8") + salt)
        user = User()
        user.password_hash = password_hash.hexdigest()
        user.email = email
        user.password_salt = salt
        user.username = username
        user.save()
        return redirect(url_for('index'))
    return render_template("register.html", title="Register")
