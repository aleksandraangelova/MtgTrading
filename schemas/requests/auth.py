from marshmallow import ValidationError, fields, validate, validates

from schemas.base import AuthBase
from utils.validations import policy


class RegisterSchemaRequest(AuthBase):
    first_name = fields.Str(required=True, validate=validate.Length(min=2, max=25))
    last_name = fields.Str(required=True, validate=validate.Length(min=2, max=25))
    city = fields.Str(required=True, validate=validate.Length(min=2, max=20))
    password = fields.Str(required=True)

    @validates("password")
    def validate_password(self, password):
        errors = policy.test(password)
        if errors:
            raise ValidationError("Password does not meet requirements")


class LoginSchemaRequest(AuthBase):
    password = fields.Str(required=True)
