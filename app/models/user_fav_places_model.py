from database import db
from sqlalchemy.dialects.postgresql import UUID
import uuid

class UserFavPlaces(db.Model):
    """SQLAlchemy model for user's favourite places table"""

    __tablename__ = "user_fav_places"

    user_id = db.Column(UUID(as_uuid=True), default=uuid.uuid4)
    places_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
