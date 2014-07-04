# -*- encoding: utf-8 -*-
import sys
import unittest
import lxml.html
from flask.ext.mongoengine import MongoEngine, MongoEngineSessionInterface

class TestSettings:
    TESTING = True
    MONGODB_SETTINGS = {'DB': 'nbtest'}
    SECRET_KEY = 'ProdaiSvoyuZebruKorove'

sys.modules['neobug.test.config'] = TestSettings
from neobug import neobug
from neobug.models import User

class NeobugTestCase(unittest.TestCase):

    def setUp(self):
        self.app = neobug.test_client()

    def tearDown(self):
        pass

    def test_register(self):
        csrf_token = self.csrf_token_register()
        rv = self.register('login', 'test@mail.com', 'proverka', csrf_token)
        assert "Add Project" in rv.data # TODO: edit this wrong assertation
        user = User.objects.get(username='login')
        user.delete()

    def test_login_logout(self):
        rv = self.login("test", "proverka")
        assert "You are logged in as" in rv.data
        rv = self.logout()
        assert "Login" in rv.data
        assert "Register" in rv.data

    def test_add_project(self):
        

    def login(self, username, password):
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def register(self, username, email, password, csrf_token):
        return self.app.post('/register', data=dict(
            username=username,
            email=email,
            password=password,
            repeat=password,
            csrf_token=csrf_token
        ), follow_redirects=True)

    def add_project(self, )

    def csrf_token_register(self):
        rv = self.app.get('/register')
        html = lxml.html.document_fromstring(rv.data)
        return html.get_element_by_id('csrf_token').value

if __name__ == "__main__":
    unittest.main()
