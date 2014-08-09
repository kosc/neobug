from flask.ext.mongoengine.wtf import model_form
from wtforms.fields import *

from models import *

PageForm = model_form(Page)
