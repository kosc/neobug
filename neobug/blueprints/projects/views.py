from flask import Blueprint, render_template, redirect, request, session

from neobug.models import Project, Issue, Comment

from forms import IssueForm, ProjectForm, CommentForm

projects = Blueprint('projects', __name__,
                     template_folder='templates')


@projects.route('/')
def index():
    project_list = Project.objects.all()
    return render_template('projects_index.html',
                           project_list=project_list)


@projects.route('/new', methods=('GET', 'POST'))
def project_new():
    project = Project()
    form = ProjectForm(request.form, project)
    if form.validate_on_submit():
        form.populate_obj(project)
        project.save()
        return redirect('/projects/')
    return render_template('projects_create.html',
                           project=project,
                           form=form)


@projects.route('/<string:project_id>', methods=('GET', 'POST'))
def project_show(project_id):
    project = Project.objects.with_id(project_id)
    issues = Issue.objects(project_id=project_id)
    for issue in issues:
        issue.comments_count = len(issue.comments)
    issue = Issue()
    form = IssueForm(request.form, issue)
    if form.validate_on_submit():
        form.populate_obj(issue)
        issue.author = session['user_id']
        issue.save()
        return redirect('/projects/' + issue.project_id)
    return render_template('projects_show.html',
                           project=project,
                           issues=issues,
                           form=form)


@projects.route('/issues/<string:issue_id>', methods=('GET', 'POST'))
def project_issue(issue_id):
    issue = Issue.objects.with_id(issue_id)
    comment = Comment()
    form = CommentForm(request.form, comment)
    if form.validate_on_submit():
        form.populate_obj(comment)
        comment.author = session['user_id']
        issue.comments.append(comment)
        issue.save()
        return redirect('/projects/issues/' + issue_id)
    return render_template('projects_issue.html',
                           issue=issue,
                           form=form)
