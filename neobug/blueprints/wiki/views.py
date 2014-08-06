from flask import Blueprint, render_template

wiki = Blueprint('wiki', __name__,
                 template_folder='templates')

@wiki.route('/')
def index():
    return render_template('wiki_layout.html', 
                           title="Wiki - main page")
