from marshmallow import Schema, fields
from schemas.pets_schema import PetsSchema
from schemas.users_schema import UsersSchema
from schemas.places_schema import PlaceSchema

class ReviewsSchema(Schema):
    """Marshmallow schema for reviews"""
    id = fields.UUID(dump_only=True)
    place_id = fields.UUID()
    user_id = fields.UUID()
    pet_id = fields.UUID()
    score = fields.Integer()
    content = fields.String()
    title = fields.String()

class ReviewsSchemaSingle(Schema):
    """Marshmallow schema for reviews"""
    id = fields.UUID(dump_only=True)
    place_id = fields.UUID()
    user_id = fields.UUID()
    pet_id = fields.UUID()
    score = fields.Integer()
    content = fields.String()
    title = fields.String()

class ReviewsInputSchema(Schema):
    """Marshmallow schema for reviews"""
    place_id = fields.UUID()
    pet_id = fields.UUID()
    score = fields.Integer()
    content = fields.String()
    title = fields.String()

    

