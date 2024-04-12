from database import db
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Reviews(db.Model):
    """SQLAlchemy model for reviews table"""

    __tablename__ = "reviews"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True))
    pet_id = db.Column(UUID(as_uuid=True))
    place_id = db.Column(UUID(as_uuid=True))
    score = db.Column(db.Integer) # out of 5
    content = db.Column(db.String, nullable=True)
    
