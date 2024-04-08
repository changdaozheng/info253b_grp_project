from marshmallow import Schema, fields

class UsersSchema(Schema):
    """Marshmallow schema for users"""
    id = fields.UUID(dump_only=True)
    username = fields.String()
    email = fields.String()
    

