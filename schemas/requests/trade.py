from marshmallow import Schema, fields


class TradeRequestSchema(Schema):
    requester_cards = fields.List(fields.Integer, required=True)
    counterparty_id = fields.Integer(required=True)
    counterparty_cards = fields.List(fields.Integer, required=True)
