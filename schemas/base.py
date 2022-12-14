from marshmallow import Schema, fields, validate
from marshmallow_enum import EnumField

from models.enum import CardCondition


class AuthBase(Schema):
    email = fields.Email(required=True)


class CardBase(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=8, max=100))
    set = fields.Str(required=True, validate=validate.Length(min=8, max=100))
    condition = EnumField(CardCondition, required=True)
    tradeable = fields.Boolean(required=True)
    foil = fields.Boolean(required=True)
