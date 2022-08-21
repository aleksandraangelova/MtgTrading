from db import db
from models.trade import Trade
from models.enum import TradeStatus


class TradeManager:

    @staticmethod
    def create(data, user):
        data["requester_id"] = user.id
        trade = Trade(**data)
        db.session.add(trade)
        return trade

    @staticmethod
    def approve_trade(trade_id):
        Trade.query.filter_by(id=trade_id).update(dict(status=TradeStatus.approved))


