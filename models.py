# -*- coding: utf-8 -*-

from flaskr import db


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    content = db.Column(db.String)

    def __init__(self, title, content):
        self.title = title
        self.content = content

    def __repr__(self):
        return '<id %r>' % self.id
