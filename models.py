from app import app
from app import db
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    orders = db.relationship('Order', backref='user', lazy=True)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stock = db.Column(db.String(255), nullable=False)
    company = db.Column(db.String(255), nullable=False)
    user_email = db.Column(db.Integer, db.ForeignKey('user.email'), nullable=False)


with app.app_context():
    db.create_all()
