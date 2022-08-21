from marshmallow import Schema, fields

from schemas.responses.card import CardResponseSchema


class TraderCardsResponseSchema(Schema):
    id = fields.Integer()
    full_name = fields.Str(required=True)
    cards = fields.List(fields.Nested(CardResponseSchema), many=True)
