from __future__ import absolute_import

import json

from app import app
from flask import render_template
from flask import url_for
from flask import redirect
from flask import abort
from flask.helpers import make_response
from flask.ext.login import current_user
from functools import wraps
from itsdangerous import URLSafeTimedSerializer
from jinja2.exceptions import TemplateNotFound


ts = URLSafeTimedSerializer(app.config["SECRET_KEY"])


def unauth_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_anonymous:
            return redirect_logged_in_user()
        return f(*args, **kwargs)
    return decorated_function


def render_path(path, **kwargs):
    try:
        return render_template(path + ".html", **kwargs)
    except TemplateNotFound:
        abort(404)


def return_success():
    return json.dumps({'success': True})


def return_error(error_message):
    return json.dumps({'error_message': error_message})


def redirect_logged_in_user():
    return redirect(url_for('index'))


def render_pdf(pdf_file, file_name=None):
    file_name = file_name or pdf_file.name
    pdf = pdf_file.read()
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = \
        'inline; filename=%s' % file_name
    return response