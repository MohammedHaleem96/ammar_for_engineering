from datetime import datetime
from app import db


class Service(db.Model):
    
    __tablename__ = 'services'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<Service {self.title}>"