#!/usr/bin/python2
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
        csrf_token = self.get_csrf_token('register')
        rv = self.register('login', 'test@mail.com', 'proverka', csrf_token)
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
        csrf_token = self.get_csrf_token('projects/new')
        name = 'New project'
        description = 'This project created for test only.'
        rv = self.add_project(name, description, csrf_token)
        assert name in rv.data
        assert description in rv.data

    def test_add_issue(self):
        self.login('test', 'proverka')
        project = Project.objects.get(name='Test project')
        project_num = project.number
        project_id = project.id
        csrf_token = self.get_csrf_token('projects/'+str(project_num))
        title = 'New issue'
        body = 'Test issue (not issue actually, huh?)'
        rv = self.add_issue(project_num, title, body, csrf_token, project_id)
        assert title in rv.data
        assert body in rv.data

    def test_add_comment(self):
        self.login('test', 'proverka')
        issue = Issue.objects.get(title='Test issue')
        issue_id = issue.number
        csrf_token = self.get_csrf_token('projects/issues/'+str(issue_id))
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

    def register(self, username, email, password, csrf_token):
        return self.app.post('/register', data=dict(
            username=username,
            email=email,
            password=password,
            repeat=password,
            csrf_token=csrf_token
        ), follow_redirects=True)

    def add_project(self, name, description, csrf_token):
        return self.app.post('/projects/new', data=dict(
            name=name,
            description=description,
            csrf_token=csrf_token
        ), follow_redirects=True)

    def add_issue(self, project_num, title, body, csrf_token, project_id):
        return self.app.post('/projects/'+str(project_num), data=dict(
            project_id=project_id,
            title=title,
            body=body,
            csrf_token=csrf_token
        ), follow_redirects=True)

    def add_comment(self, issue_id, body, csrf_token):
        return self.app.post('/projects/issues/'+str(issue_id), data=dict(
            body=body,
            csrf_token=csrf_token
        ), follow_redirects=True)

    def get_csrf_token(self, token_for):
        rv = self.app.get('/' + token_for)
        html = lxml.html.document_fromstring(rv.data)
        return html.get_element_by_id('csrf_token').value

if __name__ == '__main__':
    unittest.main()
