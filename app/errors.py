from flask import render_template

from app import db, vapp


@vapp.errorhandler(404)
def page_not_found(e):
    # This is a multiple return https://pythonbasics.org/multiple-return/
    return render_template('404.html'), 404


@vapp.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    # This is a multiple return https://pythonbasics.org/multiple-return/
    return render_template('500.html'), 500
