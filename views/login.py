from app import app, db, lm
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask import abort
from flask.ext.login import login_user
from flask.ext.login import logout_user
from models import User
from views.forms import EmailForm
from views.forms import PasswordForm
from views import utils as view_utils
from utils import ts


@app.route('/signup')
@view_utils.unauth_only
def signup():
    return render_template('signup/signup.html', next=request.values.get('next'))


@app.route('/signup/email', methods=['POST', 'GET'])
@view_utils.unauth_only
def signup_email():
    if request.method == 'POST':
        email = request.values.get('email')
        registered_user = User.query.filter_by(email=email).first()
        if registered_user:
            return _login_user()

        user = User(email=email)
        user.set_password(request.values.get('password'))
        db.session.add(user)
        db.session.commit()

        login_user(user, remember=True)

        next = request.values.get('next', url_for('index'))
        return redirect(next)
    return render_template('signup/email.html', next=request.values.get('next'))


@app.route('/signup/login', methods=['GET', 'POST'])
@view_utils.unauth_only
def signup_login():
    if request.method == 'POST':
        return _login_user()

    return render_template('signup/login.html', next=request.values.get('next'))


@app.route('/signup/reset', methods=['GET', 'POST'])
@view_utils.unauth_only
def signup_reset():
    form = EmailForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if not user:
                return render_template('signup/reset.html', form=form,
                                       error_message="Whoops, that email doesn't seem to be in our system.")

            token = ts.dumps(user.email, salt='recover-key')

            # Send the email here.
            # recover_url = url_for(
            #     'signup_reset_with_token',
            #     token=token,
            #     _external=True)
            # customer_io_logic.track_event(user.id, 'signup_reset', recover_url=recover_url)
            return render_template('signup/reset.html', form=form, success=True)

    return render_template('signup/reset.html', form=form)


@app.route('/reset/<token>', methods=["GET", "POST"])
@view_utils.unauth_only
def signup_reset_with_token(token):
    try:
        email = ts.loads(token, salt="recover-key", max_age=86400)
    except:
        abort(404)

    form = PasswordForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=email).first_or_404()

        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('signup_login'))

    return render_template('signup/reset_token.html', form=form, token=token)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


def _login_user():
    next = request.values.get('next', url_for('index'))
    email = request.form['email']
    password = request.form['password']
    registered_user = User.query.filter_by(email=email).first()
    if registered_user is None:
        flash("Whoops! We don't recognize that email.", 'error')
        return redirect(url_for('signup_login', next=next))
    if not registered_user.check_password(password):
        flash("Whoops! That password wasn't correct.", 'error')
        return redirect(url_for('signup_login', next=next))
    login_user(registered_user)

    if next:
        return redirect(next)
    return redirect(url_for('index'))