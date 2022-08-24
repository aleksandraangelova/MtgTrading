from flask import request
from flask_restful import Resource

from managers.auth import auth
from managers.trade import TradeManager
from models import Trade
from schemas.requests.trade import TradeRequestSchema
from schemas.responses.trade import (GetTradesResponseSchema,
                                     TradeBaseResponseSchema,
                                     TradeFinalizedResponseSchema)
from utils.decorators import (validate_current_user_can_see_trade_details,
                              validate_current_user_is_trade_counterparty,
                              validate_current_user_is_trade_requester,
                              validate_schema, validate_trade_status)


class TradeCreateResource(Resource):
    @auth.login_required
    @validate_schema(TradeRequestSchema)
    def post(self):
        data = request.get_json()
        current_user = auth.current_user()
        new_trade = TradeManager.create(data, current_user)
        resp = TradeBaseResponseSchema().dump(new_trade)
        return resp, 201

    @auth.login_required
    def get(self):
        current_user = auth.current_user()
        trades = TradeManager.get_trades(current_user)
        data = {"trades": trades}
        resp = GetTradesResponseSchema().dump(data)
        return resp, 200


class TradeResource(Resource):
    @auth.login_required
    @validate_current_user_can_see_trade_details()
    def get(self, trade_id):
        trade = Trade.query.filter_by(id=trade_id).first()
        return TradeBaseResponseSchema().dump(trade), 200

    @auth.login_required
    @validate_current_user_is_trade_requester()
    @validate_trade_status()
    def delete(self, trade_id):
        TradeManager.delete_trade(trade_id)
        return {"message": f"Trade {trade_id} deleted successfully"}, 200

    @auth.login_required
    @validate_schema(TradeRequestSchema)
    @validate_current_user_is_trade_requester()
    @validate_trade_status()
    def put(self, trade_id):
        data = request.get_json()
        TradeManager.update_trade(trade_id, updates_dict=data)
        return {"message": f"Trade {trade_id} updated successfully"}, 200


class ApproveTradeResource(Resource):
    @auth.login_required
    @validate_current_user_is_trade_counterparty()
    @validate_trade_status()
    def put(self, trade_id):
        TradeManager.approve_trade(trade_id)
        data = TradeManager.change_traded_cards_ownership(trade_id)
        resp = TradeFinalizedResponseSchema().dump(data)
        return resp, 200


class RejectTradeResource(Resource):
    @auth.login_required
    @validate_current_user_is_trade_counterparty()
    @validate_trade_status()
    def put(self, trade_id):
        data = TradeManager.reject_trade(trade_id)
        resp = TradeFinalizedResponseSchema().dump(data)
        return resp, 200
