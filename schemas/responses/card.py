from marshmallow import fields
from schemas.base import CardBase


class CardSchemaResponse(CardBase):
    # override the Enum definition for the response
    # it was already validated
    condition = fields.String()


