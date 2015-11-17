#!/usr/bin/python2
# -*- encoding: utf-8 -*-
import sys
import unittest
import lxml.html
from flask.ext.mongoengine import MongoEngine, MongoEngineSessionInterface

from pymongo import read_preferences


class TestSettings:
    TESTING = True
    MONGODB_SETTINGS = {
        'DB': 'nbtest',
        'read_preference': read_preferences.ReadPreference.PRIMARY
    }
    SECRET_KEY = 'ProdaiSvoyuZebruKorove'

sys.modules['neobug.test.config'] = TestSettings
from neobug import neobug
from neobug.models import User, Project, Issue


class NeobugTestCase(unittest.TestCase):

    def setUp(self):
        self.app = neobug.test_client()

    @classmethod
    def tearDownClass(self):
        user = User.objects.get(username='login')
        user.delete()
        project = Project.objects.get(name='New project')
        project.delete()
        issue = Issue.objects.get(title='New issue')
        issue.delete()
        issue = Issue.objects.get(title='Test issue')
        issue.comments = []
        issue.save()

    def test_register(self):
        csrf_token = get_csrf_token(self.app, 'register')
        rv = register(self.app, 'login', 'test@mail.com', 'proverka', csrf_token)
        assert 'login' in rv.data
        assert 'Logout' in rv.data

    def test_login_logout(self):
        rv = self.login('test', 'proverka')
        assert 'Logout(test)' in rv.data
        rv = self.logout()
        assert 'Login' in rv.data
        assert 'Register' in rv.data

    def test_add_project(self):
        self.login('test', 'proverka')
        csrf_token = get_csrf_token(self.app, 'projects/new')
        name = 'New project'
        description = 'This project created for test only.'
        rv = add_project(self.app, name, description, csrf_token)
        assert name in rv.data
        assert description in rv.data

    def test_add_issue(self):
        self.login('test', 'proverka')
        project = Project.objects.get(name='Test project')
        project_num = project.number
        project_id = project.id
        csrf_token = get_csrf_token(self.app, 'projects/'+str(project_num))
        title = 'New issue'
        body = 'Test issue (not issue actually, huh?)'
        rv = add_issue(self.app, project_num, title, body, csrf_token, project_id)
        assert title in rv.data
        assert body in rv.data

    def test_add_comment(self):
        self.login('test', 'proverka')
        issue = Issue.objects.get(title='Test issue')
        issue_id = issue.number
        csrf_token = get_csrf_token(self.app, 'projects/issues/'+str(issue_id))
        body = 'Test comment'
        rv = self.add_comment(issue_id, body, csrf_token)
        assert body in rv.data

    def login(self, username, password):
        return self.app.post('/login',
                             data=dict(username=username, password=password),
                             follow_redirects=True,
                             headers={'Referer': '/'})

    def logout(self):
        return self.app.get('/logout',
                            follow_redirects=True,
                            headers={'Referer': '/'})

    def add_comment(self, issue_id, body, csrf_token):
        return self.app.post('/projects/issues/'+str(issue_id), data=dict(
            body=body,
            csrf_token=csrf_token
        ), follow_redirects=True)


def register(app, username, email, password, csrf_token):
    return app.post('/register', data=dict(
        username=username,
        email=email,
        password=password,
        repeat=password,
        csrf_token=csrf_token
    ), follow_redirects=True)


def add_project(app, name, description, csrf_token):
    return app.post('/projects/new', data=dict(
        name=name,
        description=description,
        csrf_token=csrf_token
    ), follow_redirects=True)


def add_issue(app, project_num, title, body, csrf_token, project_id):
    return app.post('/projects/'+str(project_num), data=dict(
        project_id=project_id,
        title=title,
        body=body,
        csrf_token=csrf_token
    ), follow_redirects=True)


def get_csrf_token(app, token_for):
    rv = app.get('/' + token_for)
    html = lxml.html.document_fromstring(rv.data)
    return html.get_element_by_id('csrf_token').value

if __name__ == '__main__':
    if len(User.objects(username='test')) == 0:
        """
        We need to add test user only for first test run
        """
        app = neobug.test_client()
        token = get_csrf_token(app, 'register')
        register(app, 'test', 'test@mail.com', 'proverka', token)
        token = get_csrf_token(app, 'projects/new')
        add_project(app, 'Test project', 'Test project description', token)
        project = Project.objects(name='Test project')[0]
        project_num = project.number
        project_id = project.id
        token = get_csrf_token(app, 'projects/' + str(project_num))
        add_issue(app, project_num, 'Test issue', 'Test issue body', token, project_id)
    unittest.main()
