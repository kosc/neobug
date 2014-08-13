from flask import Blueprint, render_template, redirect, request

from models import Page
from forms import PageForm

wiki = Blueprint('wiki', __name__,
                 template_folder='templates')


@wiki.route('/')
def index():
    pages = Page.objects.all()
    return render_template('wiki_index.html',
                           title="Wiki - main page",
                           pages=pages)


@wiki.route('/edit/<string:page_id>', methods=('GET', 'POST'))
def edit(page_id):
    page = Page.objects.with_id(page_id)
    form = PageForm(request.form, page)
    if form.validate_on_submit():
        form.populate_obj(page)
        page.save()
        return redirect('/wiki/')
    return render_template('wiki_edit.html',
                           title="Wiki - edit page "+page.title,
                           page=page,
                           form=form)


@wiki.route('/create', methods=('GET', 'POST'))
def create():
    page = Page()
    form = PageForm(request.form, page)
    if form.validate_on_submit():
        form.populate_obj(page)
        page.save()
        return redirect('/wiki/')
    return render_template('wiki_create.html',
                           title="Wiki - create new page",
                           page=page,
                           form=form)


@wiki.route('/page/<string:page_id>', methods=('GET', 'POST'))
def page(page_id):
    page = Page.objects.with_id(page_id)
    return render_template('wiki_page.html',
                           page=page)
