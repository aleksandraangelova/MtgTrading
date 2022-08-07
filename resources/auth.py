from flask import request
from flask_restful import Resource

from models import TraderModel
from schemas.requests.auth import RegisterSchemaRequest, LoginSchemaRequest


class RegisterResource(Resource):
    def post(self):
        data = request.get_json()
        user = TraderModel(**data)
        return 201