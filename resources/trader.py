from flask_restful import Resource

from managers.auth import auth
from managers.card import CardManager
from managers.trader import TraderManager
from schemas.responses.trader import TraderCardsResponseSchema
from utils.decorators import validate_current_user_equals_param_uid


class TraderCardsResource(Resource):
    @auth.login_required
    @validate_current_user_equals_param_uid()
    def get(self, uid):
        cards_owned = CardManager.get_cards_owned(uid)
        full_name = TraderManager.get_full_name(uid)
        data = {"id": uid, "full_name": full_name, "cards": cards_owned}
        schema = TraderCardsResponseSchema().dump(data)
        return schema, 200