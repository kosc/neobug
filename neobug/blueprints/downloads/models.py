import hashlib
from threading import Thread

from neobug import db


class Download(db.Document):
    url = db.StringField(max_length=256, required=True)
    md5sum = db.StringField(max_length=32)
    sha1sum = db.StringField(max_length=40)
    title = db.StringField(max_length=100)
    description = db.StringField()

    def count_hash_sums(self):
        f = open('neobug/' + self.url)
        self.md5sum = hashlib.md5(f.read()).hexdigest()
        self.sha1sum = hashlib.sha1(f.read()).hexdigest()
        self.save()

    def save(self, **kwargs):
        t = Thread(target=self.count_hash_sums)
        t.start()
        super(Download, self).save(**kwargs)
