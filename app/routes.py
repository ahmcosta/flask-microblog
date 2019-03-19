import random

import lorem
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.urls import url_parse

from app import db, vapp
from app.forms import LoginForm, RegistrationForm
from app.models import User


@vapp.route('/')
@vapp.route('/index')
def index():
    user = {'username' : 'Antonio'}
    posts = [
        {
            'author': {'username': 'Henrique'},
            'body': 'Beautiful day in Brazil!'
        },
        {
            'author': {'username': 'Clara'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)


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
