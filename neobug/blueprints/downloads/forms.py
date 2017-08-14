from flask_mongoengine.wtf import model_form
from wtforms.fields import *

from neobug.blueprints.downloads.models import Download

BaseDownloadForm = model_form(Download, exclude=['md5sum', 'sha1sum'])


class DownloadForm(BaseDownloadForm):
    url = FileField('File to upload')
