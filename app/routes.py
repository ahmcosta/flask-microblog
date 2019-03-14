from app import vapp

@vapp.route('/') # Python decorator
@vapp.route('/index') # Python decorator
def index(): # This function is modified by the previous decorators
    return "Hello, world!"