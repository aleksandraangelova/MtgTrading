from marshmallow import fields, Schema
from schemas.base import CardBase


class CardResponseSchema(CardBase):
    # override the Enum definition for the response
    # it was already validated
    condition = fields.String()


class CardsTradeableSchema(CardResponseSchema):
    owner_id = fields.String()


class CardsTradeableResponseSchema(Schema):
    cards = fields.List(fields.Nested(CardBase), many=True)