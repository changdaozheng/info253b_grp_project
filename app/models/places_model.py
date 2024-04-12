from database import db

class PlaceModel(db.Model):
    """SQLAlchemy model for users table"""
    __tablename__ = "places"

    id = db.Column(db.Integer, primary_key=True)
    osmid = db.Column(db.Integer())
    lat = db.Column(db.Float())
    lng = db.Column(db.Float())
    category = db.Column(db.String())
    name = db.Column(db.String())
    city = db.Column(db.String())
    state = db.Column(db.String())
    country = db.Column(db.String())

