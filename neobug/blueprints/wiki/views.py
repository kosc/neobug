from flask import Blueprint, render_template
from models import Page
from neobug.models import Project

wiki = Blueprint('wiki', __name__,
                 template_folder='templates')

@wiki.route('/')
def index():
    projects = Project.objects.all()
    page = Page.objects.all()[0]
    return render_template('wiki_index.html',
                           title="Wiki - main page",
                           page=page)
