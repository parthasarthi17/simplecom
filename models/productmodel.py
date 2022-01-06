from init import db

class Product(db.Model):
    __tablename__ = 'product'

    id = db.Column(db.Integer, primary_key=True)
    p_name = db.Column(db.String(50))
    description = db.Column(db.String(500))
    p_image_address = db.Column(db.String(125), nullable = True)
    p_image_name = db.Column(db.String(125), nullable = True)
    brand = db.Column(db.String(50), nullable = True)
    category = db.Column(db.String(50))
    price = db.Column(db.Integer)
    discount = db.Column(db.Integer)
    speaicaloffer = db.Column(db.Boolean, default=False)
    cart = db.relationship('usercart', backref='product', lazy=True)
    ratings = db.relationship('productrating', backref='product', lazy='dynamic')
    no_ratings = db.Column(db.Integer, default = 0)
    avg_rating = db.Column(db.Float, nullable = True)
    quantity_in_store = db.Column(db.Integer)
