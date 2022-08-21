from marshmallow import Schema, fields, validate
from marshmallow_enum import EnumField

from models import TradeStatus


class TradeSchemaResponse(Schema):
    id = fields.Integer(required=True, validate=validate.Length(min=8, max=100))
    status = EnumField(TradeStatus)
    created_on = fields.DateTime()
