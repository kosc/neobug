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
from neobug.models import User, Project

class NeobugTestCase(unittest.TestCase):

    def setUp(self):
        self.app = neobug.test_client()

    def tearDown(self):
        pass

    def test_register(self):
        csrf_token = self.get_csrf_token("register")
        rv = self.register('login', 'test@mail.com', 'proverka', csrf_token)
        assert "Add Project" in rv.data
        assert 'login' in rv.data
        user = User.objects.get(username='login')
        user.delete()

    def test_login_logout(self):
        rv = self.login("test", "proverka")
        assert "You are logged in as" in rv.data
        rv = self.logout()
        assert "Login" in rv.data
        assert "Register" in rv.data

    def test_add_project(self):
        self.login("test", "proverka")
        csrf_token = self.get_csrf_token("add_project")
        name = "New project"
        description = "This project created for test only."
        rv = self.add_project(name, description, csrf_token)
        assert name in rv.data
        assert description in rv.data
        project = Project.objects.get(name=name)
        project.delete()

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

    def add_project(self, name, description, csrf_token):
        return self.app.post('/add_project', data=dict(
            name=name,
            description=description,
            csrf_token=csrf_token
        ), follow_redirects=True)

    def get_csrf_token(self, token_for):
        rv = self.app.get('/' + token_for)
        html = lxml.html.document_fromstring(rv.data)
        return html.get_element_by_id('csrf_token').value

if __name__ == "__main__":
    unittest.main()
