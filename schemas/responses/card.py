from marshmallow import fields
from marshmallow_enum import EnumField

from models import CardCondition
from schemas.base import CardBase


class CardSchemaResponse(CardBase):
    # TODO: Figure out how to use the EnumField
    condition = fields.String()


