from marshmallow import fields

from schemas.base import CardBase


class CardSchemaRequest(CardBase):
    photo = fields.String(required=True)
    extension = fields.String(required=True)