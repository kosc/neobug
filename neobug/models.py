import datetime
from flask import url_for
from neobug import db


class Project(db.Document):
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    name = db.StringField(max_length=255, required=True, unique=True)
    description = db.StringField()
    bugs = db.ListField(db.EmbeddedDocumentField('Bug'))


class Bug(db.EmbeddedDocument):
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    title = db.StringField(max_length=255, required=True)
    body = db.StringField(required=True)
    author = db.StringField(max_length=255, required=True)
    comments = db.ListField(db.EmbeddedDocumentField('Comment'))


class Comment(db.EmbeddedDocument):
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    body = db.StringField(required=True)
    author = db.StringField(max_length=255, required=True)


class User(db.Document):
    username = db.StringField(max_length=255, required=True, unique=True)
    email = db.StringField(max_length=255)
    password_hash = db.StringField(max_length=128, required=True)
    password_salt = db.StringField(max_length=32, required=True)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username
