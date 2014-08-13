from flask import Blueprint, render_template, redirect, request

from models import Download

downloads = Blueprint('downloads', __name__,
                      template_folder='templates')

@downloads.route('/')
def index():
    download_list = Download.objects.all()
    return render_template('downloads_index.html',
                           title='Downloads - main page',
                           download_list=download_list)
