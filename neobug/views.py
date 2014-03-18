from hashlib import sha512
from uuid import uuid4
from flask import Blueprint, render_template, request, url_for, redirect, session, g
from flask.ext.wtf import Form
from flask.ext.login import login_user, logout_user, current_user
from neobug import neobug
from neobug.models import *
import forms


@neobug.route('/')
@neobug.route('/index')
def index():
    projects_list = Project.objects.all()
    return render_template("index.html",
                           title="Main page",
                           projects=projects_list)


@neobug.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode('utf-8')
        user = User.objects.where("this.username=='" + username + "'")
        if len(user) == 0:
            form = forms.LoginForm(request.form, user)
            return render_template("login.html",
                                   message="Incorrect login",
                                   form=form)
        user = user[0]
        password_salt = user.password_salt.encode('utf-8')
        password_hash = sha512(password + password_salt).hexdigest()
        if password_hash == user.password_hash:
            session['logged_in'] = True
            g.user = user
            login_user(user)
            return redirect('index')
        else:
            form = forms.LoginForm(request.form, user)
            return render_template("login.html",
                                   message="Incorrect password",
                                   form=form)
    model = User()
    form = forms.LoginForm(request.form, model)
    return render_template("login.html", form=form)


@neobug.route('/logout')
def logout():
    logout_user()
    session['logged_in'] = False
    return render_template("index.html")


@neobug.route('/register', methods=('GET', 'POST'))
def register():
    user = User()
    form = forms.RegisterForm(request.form, user)
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
        salt = uuid4().hex.encode("utf-8")
        password_hash = sha512(password.encode("utf-8") + salt)
        user.password_hash = password_hash.hexdigest()
        user.email = email
        user.password_salt = salt
        user.username = username
        user.save()
        return redirect(url_for('index'))
    return render_template("register.html", title="Register", form=form)


@neobug.route('/add_project', methods=('GET', 'POST'))
def add_project():
    project = Project()
    form = forms.ProjectForm(request.form, project)
    if request.method == 'POST':
        project.name = form.data['name']
        project.description = form.data['description']
        project.save()
        return redirect(url_for('index'))
    return render_template("add_project.html", project=project, form=form)
