from database import db
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Users(db.Model):
    """SQLAlchemy model for users table"""

    __tablename__ = "users"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(), unique=True, nullable=False)
    # TODO: include authentication parameters

    reviews = db.relationship("Reviews", back_populates="user")
    