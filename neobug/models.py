import datetime
from flask import url_for
from neobug import db


class Counter(db.Document):
    id_for = db.StringField(required=True, unique=True)
    number = db.IntField(default=0, required=True)

    def __init__(self, id_for, number=0, **args):
        super(Counter, self).__init__(**args)
        self.number = number
        self.id_for = id_for

    def set_next_id(self):
        self.number += 1


class Project(db.Document):
    number = db.IntField(default=0)
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    name = db.StringField(max_length=255, required=True, unique=True)
    description = db.StringField()


class Overview(db.Document):
    content = db.StringField()


class Comment(db.EmbeddedDocument):
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    body = db.StringField(required=True)
    author = db.StringField(max_length=255, required=True)


class Issue(db.Document):
    statuses = ["New", "Rejected", "In progress", "Resolved", "Closed"]
    categories = ["Bug", "Feature", "Patch", "Pull request"]
    number = db.IntField(default=0)
    base_issue = db.IntField(default=0)
    project_id = db.StringField(max_length=24, min_length=24, required=True)
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    title = db.StringField(max_length=255, required=True)
    body = db.StringField(required=True)
    author = db.StringField(max_length=255, required=True)
    comments = db.ListField(db.EmbeddedDocumentField(Comment))
    assigned = db.StringField(max_length=255)
    status = db.StringField(max_length=12,
                            choices=statuses,
                            default=statuses[0],
                            required=True)
    category = db.StringField(max_length=13,
                              choices=categories,
                              default=categories[0],
                              required=True)


class User(db.Document):
    username = db.StringField(max_length=255, required=True, unique=True)
    email = db.StringField(max_length=255)
    admin = db.BooleanField(default=False)
    password_hash = db.StringField(max_length=128, required=True)
    password_salt = db.StringField(max_length=32, required=True)

    def is_admin(self):
        return self.admin

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username
