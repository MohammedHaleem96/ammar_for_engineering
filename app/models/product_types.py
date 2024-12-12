from flask_sqlalchemy import SQLAlchemy
from app import db


class ProductType(db.Model):
    __tablename__ = 'product_types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)

    products = db.relationship('Product', backref='type', lazy=True)
