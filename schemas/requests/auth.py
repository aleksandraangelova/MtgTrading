from marshmallow import fields, validate

from schemas.base import AuthBase


class RegisterSchemaRequest(AuthBase):
    first_name = fields.Str(required=True, validate=validate.Length(min=2, max=25))
    last_name = fields.Str(required=True, validate=validate.Length(min=2, max=25))
    city = fields.Str(required=True, validate=validate.Length(min=2, max=20))


class LoginSchemaRequest(AuthBase):
    pass
