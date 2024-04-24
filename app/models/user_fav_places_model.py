from database import db
from sqlalchemy.dialects.postgresql import UUID
import uuid

class UserFavPlaces(db.Model):
    """SQLAlchemy model for user's favourite places table"""

    __tablename__ = "user_fav_places"

    user_id = db.Column(UUID(as_uuid=True),  db.ForeignKey("users.id"), default=uuid.uuid4)
    place_id = db.Column(UUID(as_uuid=True), db.ForeignKey("places.id"),  primary_key=True, default=uuid.uuid4)

    user = db.relationship("Users")
    place = db.relationship("PlaceModel")