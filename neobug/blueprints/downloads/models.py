from neobug import db


class Download(db.Document):
    url = db.StringField(max_length=256, required=True)
    md5sum = db.StringField(max_length=32)
    sha1sum = db.StringField(max_length=40)
    title = db.StringField(max_length=100)
    description = db.StringField()
