"""
"""
from flask_login import UserMixin
from config import app, db

class User(UserMixin, db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    expenses = db.relationship('Expenses', backref='user', lazy=True)
    
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self._id)

class Expenses(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user._id'),
        nullable=False)
    product = db.Column(db.String(100))
    amount = db.Column(db.String(100))
    why = db.Column(db.String(100))

    
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self._id)

with app.app_context():
    db.create_all()
