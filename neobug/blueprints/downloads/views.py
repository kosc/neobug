import os

from flask import Blueprint, render_template, redirect, request
from werkzeug.utils import secure_filename

from neobug import neobug

from models import Download
from forms import DownloadForm

downloads = Blueprint('downloads', __name__,
                      template_folder='templates')


@downloads.route('/')
def index():
    download_list = Download.objects.all()
    return render_template('downloads_index.html',
                           download_list=download_list)


@downloads.route('/new', methods=('GET', 'POST'))
def downloads_new():
    download = Download()
    form = DownloadForm(request.form, download)
    if form.validate_on_submit():
        f = request.files['url']
        if f:
            filename = secure_filename(f.filename)
            f.save(os.path.join(neobug.config['UPLOAD_FOLDER'], filename))
            form.populate_obj(download)
            download.url = 'static/uploads/' + filename
            download.save()
        return redirect('/downloads')
    return render_template('downloads_new.html',
                           form=form)
