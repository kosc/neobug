from neobug import db

class Page(db.Document):
    title = db.StringField(max_length=200)
    content = db.StringField()
