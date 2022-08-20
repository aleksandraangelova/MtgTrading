from db import db
from models.trade import Trade


class TradeManager:

    @staticmethod
    def create(data, user):
        data["requester_id"] = user.id
        trade = Trade(**data)
        db.session.add(trade)
        return trade
