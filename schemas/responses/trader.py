from marshmallow import Schema, fields

from schemas.responses.card import CardSchemaResponse


class TraderCardsResponseSchema(Schema):
    id = fields.Integer()
    # TODO: return full_name
    cards = fields.List(fields.Nested(CardSchemaResponse), many=True)
