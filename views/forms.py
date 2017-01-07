from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired
from wtforms.validators import Email


class EmailForm(Form):
    email = StringField('email', validators=[DataRequired(), Email()])


class PasswordForm(Form):
    password = StringField('password', validators=[DataRequired()])