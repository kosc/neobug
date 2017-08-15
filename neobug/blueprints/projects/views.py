from flask import Blueprint, render_template, redirect, request, session

from neobug.models import Project, Issue, Comment, Counter

from neobug.blueprints.projects.forms import IssueForm, ProjectForm, CommentForm

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
    form = ProjectForm(request.form)
    if form.validate_on_submit():
        if Counter.objects(id_for="project").count() == 0:
            counter = Counter("project")
            counter.save()
        else:
            counter = Counter.objects(id_for="project")[0]
            counter.set_next_id()
            counter.save()
        form.populate_obj(project)
        project.number = counter.number
        project.save()
        return redirect('/projects/')
    return render_template('projects_create.html',
                           project=project,
                           form=form)


@projects.route('/<string:num>', methods=('GET', 'POST'))
def project_show(num):
    project = Project.objects(number=num)[0]
    issues = Issue.objects(project_id=str(project.id))
    for issue in issues:
        issue.comments_count = len(issue.comments)
    issue = Issue()
    form = IssueForm(request.form)
    if form.validate_on_submit():
        if Counter.objects(id_for="issue").count() == 0:
            counter = Counter("issue")
            counter.save()
        else:
            counter = Counter.objects(id_for="issue")[0]
            counter.set_next_id()
            counter.save()
        form.populate_obj(issue)
        issue.number = counter.number
        issue.author = session['user_id']
        issue.save()
        return redirect('/projects/' + str(project.number))
    return render_template('projects_show.html',
                           project=project,
                           issues=issues,
                           form=form)


@projects.route('/issues/<string:num>', methods=('GET', 'POST'))
def project_issue(num):
    issue = Issue.objects(number=num)[0]
    child_issues = Issue.objects(base_issue=num)
    comment = Comment()
    form = CommentForm(request.form)
    if form.validate_on_submit():
        form.populate_obj(comment)
        comment.author = session['user_id']
        issue.comments.append(comment)
        issue.save()
        return redirect('/projects/issues/' + num)
    return render_template('projects_issue.html',
                           issue=issue,
                           child_issues=child_issues,
                           form=form)


@projects.route('/issues/<string:num>/child', methods=('GET', 'POST'))
def projects_childissue(num):
    base_issue = Issue.objects(number=num)[0]
    project = Project.objects(id=base_issue.project_id)[0]
    issue = Issue()
    form = IssueForm(request.form)
    if form.validate_on_submit():
        form.populate_obj(issue)
        counter = Counter.objects(id_for="issue")[0]
        counter.set_next_id()
        counter.save()
        issue.number = counter.number
        issue.author = session['user_id']
        issue.base_issue = num
        issue.save()
        return redirect('projects/issues/' + str(num))
    return render_template(
                'projects_childissue.html',
                project=project,
                base_issue=base_issue,
                issue=issue,
                form=form)
