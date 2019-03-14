from flask import render_template
from app import vapp
@vapp.route('/')
@vapp.route('/index')
def index():
    user = {'username' : 'Antonio'}
    return render_template('index.html', title = 'Home', user = user)