from flask import request
from flask_restful import Resource

from managers.auth import auth
from managers.card import CardManager
from schemas.requests.card import CardSchemaRequest
from schemas.responses.card import (CardResponseSchema,
                                    CardsTradeableResponseSchema)
from utils.decorators import validate_schema


class CardResource(Resource):
    @auth.login_required
    @validate_schema(CardSchemaRequest)
    def post(self):
        data = request.get_json()
        current_user = auth.current_user()
        new_card = CardManager.create(data, current_user)
        return CardResponseSchema().dump(new_card), 201


class CardsTradeableResource(Resource):
    @auth.login_required
    def get(self):
        uid = auth.current_user().id
        cards = CardManager.get_cards_for_trade(uid)
        data = {"cards": cards}
        resp = CardsTradeableResponseSchema().dump(data)
        return resp, 200
