# -*- coding: utf-8 -*-
"""
    Flaskr Tests
    ~~~~~~~~~~~~

    Tests the Flaskr application.

    :copyright: (c) 2010 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
"""
import os
import flaskr
import unittest
import tempfile



from flask import template_rendered
from contextlib import contextmanager
@contextmanager
def captured_templates(app):
    recorded = []
    def record(sender, template, context, **extra):
        recorded.append((template, context))
    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        """Before each test, set up a blank database"""
        self.db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
        flaskr.app.config['TESTING'] = True
        self.app = flaskr.app.test_client()


    def tearDown(self):
        """Get rid of the database again after each test."""
        os.close(self.db_fd)
        os.unlink(flaskr.app.config['DATABASE'])

    def login(self, username, password):
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    # testing functions

    def test_empty_db(self):
        """Start with a blank database."""
        with captured_templates(flaskr.app) as templates:
            rv = flaskr.app.test_client().get('/')
            assert rv.status_code == 200
            assert len(templates) == 1
            template, context = templates[0]
            print template.name
            #print len(context['items'])

    def test_login_logout(self):
        """Make sure login and logout works"""
        rv = self.login(flaskr.app.config['USERNAME'],
                        flaskr.app.config['PASSWORD'])
        assert 'You were logged in' in rv.data
        rv = self.logout()
        assert 'You were logged out' in rv.data
        rv = self.login(flaskr.app.config['USERNAME'] + 'x',
                        flaskr.app.config['PASSWORD'])
        assert 'Invalid username' in rv.data
        rv = self.login(flaskr.app.config['USERNAME'],
                        flaskr.app.config['PASSWORD'] + 'x')
        assert 'Invalid password' in rv.data

    def test_messages(self):
        """Test that messages work"""
        self.login(flaskr.app.config['USERNAME'],
                   flaskr.app.config['PASSWORD'])
        rv = self.app.post('/add', data=dict(
            title='<Hello>',
            text='<strong>HTML</strong> allowed here'
        ), follow_redirects=True)
        #assert 'No entries here so far' not in rv.data
        #assert '&lt;Hello&gt;' in rv.data
        #assert '<strong>HTML</strong> allowed here' in rv.data


if __name__ == '__main__':
    unittest.main()
