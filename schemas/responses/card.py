from marshmallow import fields

from schemas.base import CardBase


class CardSchemaResponse(CardBase):
    id = fields.Int(required=True)
    photo_url = fields.String(required=True)
    # TODO: make nested schema for complainer obj
    # complainer = fields.Nested()

