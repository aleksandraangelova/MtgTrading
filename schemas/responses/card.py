from marshmallow import Schema, fields

from schemas.base import CardBase


class CardSchemaResponse(Schema):
    # TODO: Figure out how to parse enum field
    id = fields.Int(required=True)
    photo_url = fields.String(required=True)


