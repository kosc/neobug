from flask import Blueprint, render_template, redirect, request
from neobug.models import Project
from models import Page
from forms import PageForm

wiki = Blueprint('wiki', __name__,
                 template_folder='templates')

@wiki.route('/')
def index():
    projects = Project.objects.all()
    page = Page.objects.all()[0]
    return render_template('wiki_index.html',
                           title="Wiki - main page",
                           page=page)

@wiki.route('/edit/<string:page_id>', methods=('GET', 'POST'))
def edit(page_id):
    page = Page.objects.with_id(page_id)
    form = PageForm(request.form, page)
    if form.validate_on_submit():
        form.populate_obj(page)
        page.save()
        return redirect('/')
    return render_template('wiki_edit.html',
                           title="Wiki - edit page "+page.title,
                           page=page,
                           form=form)
