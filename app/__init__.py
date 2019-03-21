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

# routes modules is imported at the bottom (NOT at the top)
# It avoids circular imports, a commom problem with Flask applications
from app import routes, models, errors  # isort:skiped
