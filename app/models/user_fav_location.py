from database import db
from sqlalchemy.dialects.postgresql import UUID
import uuid

class UserFavLocations(db.Model):
    """SQLAlchemy model for user's favourite locations table"""

    __tablename__ = "user_fav_locations"

    user_id = db.Column(UUID(as_uuid=True), default=uuid.uuid4)
    places_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
