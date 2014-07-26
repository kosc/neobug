from hashlib import sha512
from uuid import uuid4
from flask_pymongo import ObjectId
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
    model = User()
    login_form = forms.LoginForm(request.form, model)
    return render_template("index.html",
                           title="Main page",
                           projects=projects_list,
                           login_form=login_form)


@neobug.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode('utf-8')
        user = User.objects.where("this.username=='" + username + "'")
        if len(user) == 0:
            login_form = forms.LoginForm(request.form, user)
            return render_template("login.html",
                                   message="Incorrect login",
                                   login_form=login_form)
        user = user[0]
        password_salt = user.password_salt.encode('utf-8')
        password_hash = sha512(password + password_salt).hexdigest()
        if password_hash == user.password_hash:
            session['logged_in'] = True
            g.user = user
            login_user(user)
            return redirect('index')
        else:
            login_form = forms.LoginForm(request.form, user)
            return render_template("login.html",
                                   message="Incorrect password",
                                   login_form=login_form)
    model = User()
    login_form = forms.LoginForm(request.form, model)
    return render_template("login.html", login_form=login_form)


@neobug.route('/logout')
def logout():
    logout_user()
    session['logged_in'] = False
    return redirect('index')


@neobug.route('/register', methods=('GET', 'POST'))
def register():
    user = User()
    form = forms.RegisterForm(request.form, user)
    login_form = forms.LoginForm(request.form, user)
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
        session['logged_in'] = True
        g.user = user
        login_user(user)
        return redirect(url_for('index'))
    return render_template("register.html", 
                           title="Register", 
                           form=form,
                           login_form=login_form)


@neobug.route('/add_project', methods=('GET', 'POST'))
def add_project():
    project = Project()
    form = forms.ProjectForm(request.form, project)
    if request.method == 'POST':
        form.populate_obj(project)
        project.save()
        return redirect(url_for('index'))
    return render_template("add_project.html", 
                           project=project, 
                           form=form)


@neobug.route('/projects/<string:project_id>', methods=('GET', 'POST'))
def bugs(project_id):
    project = Project.objects.with_id(project_id)
    bugs = Bug.objects.where("this.project_id=='" + project_id + "'")
    for bug in bugs:
        bug.comments_count = len(bug.comments)
    bug = Bug()
    form = forms.BugForm(request.form, bug)
    user = User()
    login_form = forms.LoginForm(request.form, user)
    if form.validate_on_submit():
        form.populate_obj(bug)
        bug.author = session['user_id']
        bug.save()
        return redirect('/projects/' + bug.project_id)
    return render_template("bugs.html", 
                           project=project, 
                           bugs=bugs, 
                           form=form, 
                           login_form=login_form)


@neobug.route('/bugs/<string:bug_id>', methods=('GET', 'POST'))
def bug(bug_id):
    bug = Bug.objects.with_id(bug_id)
    comment = Comment()
    form = forms.CommentForm(request.form, comment)
    user = User()
    login_form = forms.LoginForm(request.form, comment)
    if form.validate_on_submit():
        form.populate_obj(comment)
        comment.author = session['user_id']
        bug.comments.append(comment)
        bug.save()
        return redirect('/bugs/' + bug_id)
    return render_template("comments.html", 
                           bug=bug, 
                           form=form, 
                           login_form=login_form)
