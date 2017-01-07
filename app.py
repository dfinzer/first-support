import os
from flask.helpers import url_for
import redis
import utils

from flask import Flask
from flask.ext.login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__, static_folder='assets')
app.config.from_object(os.environ['APP_SETTINGS'])


def dated_url_for(endpoint, **values):
    if endpoint == 'static' and utils.on_heroku():
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)


# Static asset cache busting.
@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)


# Database.
db = SQLAlchemy(app)
lm = LoginManager(app)
lm.login_view = 'signup_login'


# Redis.
r = redis.from_url(app.config["REDISTOGO_URL"])