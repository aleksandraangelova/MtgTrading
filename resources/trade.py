from flask import request
from flask_restful import Resource

from managers.auth import auth
from managers.trade import TradeManager
from models import Trade
from schemas.base import TradeBase
from schemas.responses.trade import TradeSchemaResponse
from utils.decorators import (validate_current_user_can_see_trade_details,
                              validate_current_user_is_trade_counterparty,
                              validate_schema)


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
    @validate_current_user_can_see_trade_details()
    def get(self, trade_id):
        # TODO: Put in manager
        trade = Trade.query.filter_by(id=trade_id).first()
        return TradeSchemaResponse().dump(trade), 201


class ApproveTradeResource(Resource):
    @auth.login_required
    @validate_current_user_is_trade_counterparty()
    def put(self, trade_id):
        return 201
