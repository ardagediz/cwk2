from app import db
from flask_login import UserMixin

# Association table for the many-to-many relationship
wishlist = db.Table(
    'wishlist',
    db.Column('user_id', db.Integer, db.ForeignKey(
        'user.id'), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey(
        'product.id'), primary_key=True)
)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    wishlisted_products = db.relationship(
        'Product',
        secondary=wishlist,
        backref=db.backref('users', lazy='dynamic')
    )


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)
    likes = db.Column(db.Integer, default=0, nullable=False)
