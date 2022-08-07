from flask import request
from flask_restful import Resource

from managers.trader import TraderManager
from models import TraderModel
from schemas.requests.auth import RegisterSchemaRequest, LoginSchemaRequest


class RegisterResource(Resource):
    def post(self):
        data = request.get_json()
        token = TraderManager.register(data)
        return {"token": token}, 201


class LoginResource(Resource):
    def post(self):
        data = request.get_json()
        token = TraderManager.login(data)
        return {"token": token}, 200
