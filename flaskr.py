# -*- coding: utf-8 -*-

from flask import Flask, request, session, redirect, url_for, abort, flash, render_template, current_app
from flask.ext.sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension
import time
from datetime import date
from datetime import datetime
import logging
from logging.handlers import WatchedFileHandler
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
# create our little application :)
app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
moment = Moment(app)
db = SQLAlchemy(app)
#toolbar = DebugToolbarExtension(app)
bootstrap = Bootstrap(app)
from models import *

@app.route('/path/<name>')
def redirect(name):
    return render_template('bootstrap.html', name= name, dt=datetime.utcnow() )


@app.route('/')
def show_entries():
    app.logger.info(app.config["DEBUG"])
    return render_template('show_entries.html', entries=Post.query.all())


@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    post = Post(request.form["title"], request.form["content"])
    db.session.add(post)
    db.session.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin':
            error = 'Invalid username'
        elif request.form['password'] != 'admin':
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))


if __name__ == '__main__':
    file_handler = logging.FileHandler("log.txt")
    file_handler.setLevel(logging.DEBUG)
    app.logger.addHandler(file_handler)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    app.logger.addHandler(console_handler)
    app.logger.setLevel(logging.DEBUG)
    app.logger.info(__name__)
    app.run()