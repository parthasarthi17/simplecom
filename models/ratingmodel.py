from init import db

from models.usermodel import User
from models.productmodel import Product

class productrating(db.Model):
    __tablename__ = 'productrating'
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'),nullable=False)
