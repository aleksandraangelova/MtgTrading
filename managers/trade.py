from db import db
from models.trade import Trade
from models.card import Card
from models.enum import TradeStatus
from utils.common import get_trade


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

    @staticmethod
    def change_traded_cards_ownership(trade_id):
        trade = get_trade(trade_id)
        cards_for_requester, requester_id = trade.counterparty_cards, trade.requester_id
        for card in cards_for_requester:
            Card.query.filter_by(id=card).update(dict(owner_id=requester_id, tradeable=False))








