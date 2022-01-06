from init import db

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(25))
    username = db.Column(db.String(40), unique=True)
    password = db.Column(db.String(15))
    user_city = db.Column(db.String(25))
    user_address = db.Column(db.String(50))
    authenticated = db.Column(db.Boolean, default=False)
    staff = db.Column(db.Boolean, default=False)
    vendor = db.Column(db.Boolean, default=False)
    brand  = db.Column(db.String(25))
    userpoints = db.Column(db.Integer)
    cart = db.relationship('usercart', backref='user', lazy=True)
    rate_products = db.relationship('productrating', backref='user', lazy='dynamic')

    def is_active(self):
        return True

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return self.authenticated

    def is_staff(self):
        return self.staff

    def is_vendor(self):
        return self.vendor

    def is_anonymous(self):
        return False
