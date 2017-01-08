import json
import os

from app import app
from app import db
from flask.ext.script import Manager
from flask.ext.migrate import Migrate
from flask.ext.migrate import MigrateCommand


app.config.from_object(os.environ['APP_SETTINGS'])

from app import r

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

@manager.command
def dump_json():
    with open('uploads/output.json', 'w') as f:
        f.write(json.dumps(r.lrange("mood_points", 0, -1)))

@manager.command
def flush_db():
    r.flushdb()

if __name__ == '__main__':
    manager.run()