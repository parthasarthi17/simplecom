from init import db

from models.usermodel import User
from models.productmodel import Product

class usercart(db.Model):
    __tablename__ = 'usercart'
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'),nullable=False)
    product_qty = db.Column(db.Float)
    total = db.Column(db.Float)
    status = db.Column(db.String(40), default = "Shopping")
