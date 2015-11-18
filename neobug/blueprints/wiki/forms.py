from flask.ext.mongoengine.wtf import model_form
from wtforms.fields import *

from neobug.blueprints.wiki.models import *

PageForm = model_form(Page)
