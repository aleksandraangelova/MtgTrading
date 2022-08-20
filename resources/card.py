from flask import request
from flask_restful import Resource

from managers.auth import auth
from managers.card import CardManager
from models import UserRole
from schemas.requests.card import CardSchemaRequest
from schemas.responses.card import CardSchemaResponse

from utils.decorators import permission_required, validate_schema


class CardResource(Resource):
    @auth.login_required
    @validate_schema(CardSchemaRequest)
    def post(self):
        data = request.get_json()
        current_user = auth.current_user()
        new_card = CardManager.create(data, current_user)
        return CardSchemaResponse().dump(new_card), 201
