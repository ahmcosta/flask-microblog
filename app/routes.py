from flask import render_template
from app import vapp
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