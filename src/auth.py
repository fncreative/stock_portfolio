from flask import flash, render_template, redirect, url_for, session, g
from . import app
from .forms import AuthForm
from .models import Account, db
import functools


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.get('account') is None:
            flash('You must be logged in to visit this page.')
            return redirect(url_for('.login'))

        return view(**kwargs)

    return wrapped_view


@app.before_request
def load_logged_in_account():
    """ Get account id from session """
    account_id = session.get('account_id')

    if account_id is None:
        g.account = None
    else:
        g.account = Account.query.get(account_id)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = AuthForm()

    if form.validate_on_submit():
        email = form.data['email']
        password = form.data['password']
        error = None

        if not email or not password:
            error = 'Invalid email or password'

        if Account.query.filter_by(email=email).first() is not None:
            error = f'{ email } has already been registered'

        if error is None:
            account = Account(email=email, password=password)
            db.session.add(account)
            db.session.commit()

            flash('Registration complete')
            return redirect(url_for('.login'))

        flash(error)

    return render_template('auth/register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = AuthForm()

    if form.validate_on_submit():
        email = form.data['email']
        password = form.data['password']
        error = None

        account = Account.query.filter_by(email=email).first()

        if account is None or not Account.check_password_hash(account, password):
            error = 'invalid username or password'

        if error is None:
            session.clear()
            session['account_id'] = account.id
            print(session['account_id'])
            flash('You have logged in successfully')
            return redirect(url_for('.home'))

        flash(error)

    return(render_template('auth/login.html', form=form))


@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out')
    return redirect(url_for('.login'))
