from marshmallow import Schema, fields, validate
from marshmallow_enum import EnumField

from models import TradeStatus


class TradeBaseResponseSchema(Schema):
    id = fields.Integer(required=True, validate=validate.Length(min=8, max=100))
    status = EnumField(TradeStatus)
    created_on = fields.DateTime()


class TradeFinalizedResponseSchema(TradeBaseResponseSchema):
    transferred_to_requester = fields.List(fields.Int)
    transferred_to_counterparty = fields.List(fields.Int)


class TradeResponseSchema(TradeBaseResponseSchema):
    requester_id = fields.Integer()
    counterparty_id = fields.Integer()
    requester_cards = fields.List(fields.Int)
    counterparty_cards = fields.List(fields.Int)


class GetTradesResponseSchema(Schema):
    trades = fields.List(fields.Nested(TradeResponseSchema), many=True)