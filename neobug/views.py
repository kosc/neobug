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
    current_page = request.referrer
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
            return redirect(current_page)
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
    current_page = request.referrer
    logout_user()
    session['logged_in'] = False
    return redirect(current_page)


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
def issues(project_id):
    project = Project.objects.with_id(project_id)
    issues = Issue.objects.where("this.project_id=='" + project_id + "'")
    for issue in issues:
        issue.comments_count = len(issue.comments)
    issue = Issue()
    form = forms.IssueForm(request.form, issue)
    user = User()
    login_form = forms.LoginForm(request.form, user)
    if form.validate_on_submit():
        form.populate_obj(issue)
        issue.author = session['user_id']
        issue.save()
        return redirect('/projects/' + issue.project_id)
    return render_template("issues.html",
                           project=project,
                           issues=issues,
                           form=form,
                           login_form=login_form)


@neobug.route('/issues/<string:issue_id>', methods=('GET', 'POST'))
def issue(issue_id):
    issue = Issue.objects.with_id(issue_id)
    comment = Comment()
    form = forms.CommentForm(request.form, comment)
    user = User()
    login_form = forms.LoginForm(request.form, comment)
    if form.validate_on_submit():
        form.populate_obj(comment)
        comment.author = session['user_id']
        issue.comments.append(comment)
        issue.save()
        return redirect('/issues/' + issue_id)
    return render_template("comments.html",
                           issue=issue,
                           form=form,
                           login_form=login_form)


@neobug.route('/close_issue/<string:issue_id>', methods=('GET', 'POST'))
def close_issue(issue_id):
    if request.method == 'GET':
        issue = Issue.objects.with_id(issue_id)
        issue.is_closed = True
        issue.save()
    else:
        return "Error! Something goes wrong here..."
    return redirect('/projects/' + issue.project_id)
