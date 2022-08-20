from db import db
from models.trade import Trade
from utils.decorators import validate_current_user_equals_param_uid


class TradeManager:

    @staticmethod
    def create(data, user):
        data["requester_id"] = user.id
        trade = Trade(**data)
        db.session.add(trade)
        return trade
