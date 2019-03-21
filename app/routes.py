import random
from datetime import datetime

import lorem
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.urls import url_parse

from app import db, vapp
from app.forms import EditProfileForm, LoginForm, RegistrationForm
from app.models import User


@vapp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@vapp.route('/')
@vapp.route('/index')
@login_required
def index():
    posts = [
        {
            'author': {'username': 'Antonio'},
            'body': 'Beautiful day in Brazil!'
        },
        {
            'author': {'username': 'Clara'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', posts=posts)


@vapp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@vapp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@vapp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


# route has a dynamic component, Flask will accept any 
# text in that portion of the URL
@vapp.route('/user/<username>')
@login_required
def user(username):
    # first_or_404() works exactly like first() when there 
    # are results, but in the case that there are no results 
    # automatically sends a 404 error back to the client
    user = User.query.filter_by(username=username).first_or_404()
    number = random.randint(1, 3)
    posts = []
    print('Number: ', number)
    print('Range: ', range(number))
    for n in range(number):
        posts.append({
            'author': user,
            'body': lorem.text(),
        })
    return render_template('user.html', user=user, posts=posts)


@vapp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        # It's not necessary, because when current_user is
        # referenced, Flask-login will invoke the user
        # loader callback function
        # db.session.add() # <<<
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)
