from database import db
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Pets(db.Model):
    """SQLAlchemy model for pets table"""

    __tablename__ = "pets"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("users.id"))
    name = db.Column(db.String(50), unique=True, nullable=False)
    breed = db.Column(db.String(50), unique=True, nullable=False)
    
    user = db.relationship("Users")