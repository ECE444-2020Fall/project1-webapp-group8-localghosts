from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from . import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    """Flask-login required function.

    Args:
        user_id: the id of the user.

    Returns:
        The User object associated with the id.

    """
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    """A User of the application.

    Attributes:
        id: the user's unique id
        email: the user's email (up to 254 characters)
        username: the user's username (up to 64 characters)
        password_hash: the user's password stored as a hash (using Werkzeug security)
    """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(254), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return "<User %r>" % self.username

    @property
    def password(self):
        """
        Raises:
            AttributeError: If an unauthorized password access is attempted.
        """
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password):
        """Sets the password attribute to the given password's hash

        Args:
            password: The new password to set the hash to.
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """Checks if the stored password hash matches that of the given one.

        Args:
            password: the password to compare to the stored hash.
        """
        return check_password_hash(self.password_hash, password)
