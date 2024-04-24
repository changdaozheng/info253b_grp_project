from marshmallow import Schema, fields




class PlaceSchema(Schema):
    """Marshmallow schema for places"""
    id = fields.UUID(dump_only=True)
    osmid = fields.Integer(required=True)
    name = fields.String(required=True)
    lat = fields.Float(required=True)
    lng = fields.Float(required=True)
    category = fields.String(required=True)
    city = fields.String(required=True)
    state = fields.String(required=True)
    country = fields.String(required=True)

class PlaceUpdateSchema(Schema):
    """Marshmallow schema for updating places"""
    osmid = fields.Integer()
    name = fields.String()
    lat = fields.Float()
    lng = fields.Float()
    category = fields.String()
    city = fields.String()
    state = fields.String()
    country = fields.String()
