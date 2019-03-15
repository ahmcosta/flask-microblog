from app import db, vapp
from app.models import Post, User


@vapp.shell_context_processor
def make_shell_context():
    return {
        'db': db, 'User': User, 'Post': Post
    }
