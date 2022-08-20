from flask import request
from flask_restful import Resource
from werkzeug.exceptions import Forbidden

from managers.auth import auth
from managers.trade import TradeManager
from models import UserRole, Trade
from schemas.responses.trade import TradeSchemaResponse
from schemas.base import TradeBase

from utils.decorators import permission_required, validate_schema


class TradeResource(Resource):
    @auth.login_required
    @validate_schema(TradeBase)
    def post(self):
        data = request.get_json()
        current_user = auth.current_user()
        new_trade = TradeManager.create(data, current_user)
        # TODO: Figure out how to return the id and status
        return 201


class TradeDetailsResource(Resource):
    @auth.login_required
    def get(self, trade_id):
        trade = Trade.query.filter_by(id=trade_id).first()
        uid = auth.current_user().id
        if trade.requester_id == uid:
            return TradeSchemaResponse().dump(trade), 201
        else:
            raise Forbidden("Permission denied")
