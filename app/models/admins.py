from flask_login import UserMixin
from werkzeug.security import generate_password_hash
#from flask_sqlalchemy import SQLAlchemy
from app import db


class Admin(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    def __init__(self, username, password_hash):
        self.username = username
        self.password_hash = password_hash

    def set_password(self, password):
        """Hash the password before storing it in the database."""
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        """Check if the given password matches the stored hash."""
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password_hash, password)

