from init import db

class Images(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(120), nullable=False)
    data  = db.Column(db.LargeBinary )
