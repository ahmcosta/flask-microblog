import logging
import os
from logging.handlers import RotatingFileHandler, SMTPHandler

from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config

# __name__ Python predefined variable, which is set
#  to the name of the module in which it is used.
vapp = Flask(__name__)
vapp.config.from_object(Config)
db = SQLAlchemy(vapp)  # db is the object that represents the database
migrate = Migrate(vapp, db)  # db is the object that represents the database
login = LoginManager(vapp)
login.login_view = 'login'

if not vapp.debug:
    if vapp.config['MAIL_SERVER']:
        auth = None
        if vapp.config['MAIL_USERNAME'] or vapp.config['MAIL_PASSWORD']:
            auth = (vapp.config['MAIL_USERNAME'], vapp.config['MAIL_PASSWORD'])
        secure = None
        if vapp.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(vapp.config['MAIL_SERVER'], vapp.config['MAIL_PORT']),
            fromaddr='no-reply@' + vapp.config['MAIL_SERVER'],
            toaddrs=vapp.config['ADMINS'], subject='Microblog Failure',
            credentials=auth, secure=secure)
        mail_handler.setLevel(logging.ERROR)
        vapp.logger.addHandler(mail_handler)

    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240,
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    vapp.logger.addHandler(file_handler)

    vapp.logger.setLevel(logging.INFO)
    vapp.logger.info('Microblog startup')

# routes modules is imported at the bottom (NOT at the top)
# It avoids circular imports, a commom problem with Flask applications
from app import routes, models, errors  # isort:skiped
