from flask_restful import Resource

from managers.auth import auth
from managers.card import CardManager
from schemas.responses.trader import TraderCardsResponseSchema
from utils.decorators import permission_required


class TraderCardsResource(Resource):
    @auth.login_required
    @permission_required()
    def get(self, uid):
        cards_owned = CardManager.get_cards_owned(uid)
        data = {"id": uid, "cards": cards_owned}
        schema = TraderCardsResponseSchema().dump(data)
        return schema, 201