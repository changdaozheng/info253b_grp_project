from marshmallow import Schema, fields

class UsersSchema(Schema):
    """Marshmallow schema for users"""
    id = fields.UUID(dump_only=True)
    username = fields.String()
    email = fields.String()

class UserFavPlacesSchema(Schema):
    """Marshmallow schema for operations on user's favourite places"""
    user_id = fields.UUID()
    place_id = fields.UUID()