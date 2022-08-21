from marshmallow import fields, Schema
from schemas.base import CardBase


class CardResponseSchema(CardBase):
    # override the Enum definition for the response
    # it was already validated
    condition = fields.String()


class CardsTradeableSchema(CardBase):
    owner_id = fields.String()


class CardsTradeableResponseSchema(Schema):
    cards = fields.List(fields.Nested(CardsTradeableSchema), many=True)