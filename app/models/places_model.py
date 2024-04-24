from database import db
from sqlalchemy.dialects.postgresql import UUID
import uuid


class PlaceModel(db.Model):
    """SQLAlchemy model for users table"""
    __tablename__ = "places"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    osmid = db.Column(db.Integer())
    lat = db.Column(db.Float())
    lng = db.Column(db.Float())
    category = db.Column(db.String())
    name = db.Column(db.String())
    city = db.Column(db.String())
    state = db.Column(db.String())
    country = db.Column(db.String())

