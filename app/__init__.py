from flask import Flask

# __name__ Python predefined variable, which is set
#  to the name of the module in which it is used.
vapp = Flask(__name__)

# routes modules is imported at the bottom (NOT at the top)
# It avoids circular imports, a commom problem with Flask applications
from app import routes