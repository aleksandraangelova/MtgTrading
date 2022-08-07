from flask import request
from flask_restful import Resource

from managers.trader import TraderManager
from schemas.requests.auth import RegisterSchemaRequest, LoginSchemaRequest
from utils.decorators import validate_schema


class RegisterResource(Resource):
    @validate_schema(RegisterSchemaRequest)
    def post(self):
        data = request.get_json()
        token = TraderManager.register(data)
        return {"token": token}, 201


class LoginResource(Resource):
    @validate_schema(LoginSchemaRequest)
    def post(self):
        data = request.get_json()
        token = TraderManager.login(data)
        return {"token": token}, 200
