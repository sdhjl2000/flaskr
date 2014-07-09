from flask.ext.script import Manager, Shell, Server
from flask.ext.migrate import Migrate, MigrateCommand
from flaskr import app, db

import os

app.config.from_object('config.DevelopmentConfig')

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)
manager.add_command("runserver", Server())
manager.add_command("shell", Shell())
if __name__ == '__main__':
    manager.run()
