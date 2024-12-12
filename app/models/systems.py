from flask_sqlalchemy import SQLAlchemy
from app.models.products import Product
from app import db

class System(db.Model):
    __tablename__ = 'systems'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    install_price = db.Column(db.Numeric(10, 2))
    total_price = db.Column(db.Numeric(10, 2))
    
    products = db.relationship('Product', secondary='system_products', backref=db.backref('systems', lazy='dynamic'))

    def calculate_total_price(self):
        """Calculate the total price of the system based on the prices of the products."""
        self.total_price = sum(product.price for product in self.products) + self.install_price
        db.session.commit()
    
    def add_product(self, product, quantity=1):
        """Add a product to the system."""
        system_product = SystemProduct(system_id=self.id, product_id=product.id, quantity=quantity)
        db.session.add(system_product)
        self.calculate_total_price()
        db.session.commit()
    
    def remove_product(self, product):
        """Remove a product from the system."""
        system_product = SystemProduct.query.filter_by(system_id=self.id, product_id=product.id).first()
        if system_product:
            db.session.delete(system_product)
            self.calculate_total_price()
            db.session.commit()

class SystemProduct(db.Model):
    __tablename__ = 'system_products'
    system_id = db.Column(db.Integer, db.ForeignKey('systems.id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), primary_key=True)
    quantity = db.Column(db.Integer, default=1)

    system = db.relationship('System', backref=db.backref('system_products', lazy=True))
    product = db.relationship('Product', backref=db.backref('system_products', lazy=True))