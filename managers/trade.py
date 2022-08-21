from werkzeug.exceptions import Forbidden

from db import db
from models.card import Card
from models.enum import TradeStatus
from models.trade import Trade
from utils.common import get_trade


class TradeManager:
    @staticmethod
    def create(data, user):

        if data["counterparty_id"] == user.id:
            raise Forbidden("Trade denied. You cannot make a trade with yourself!")

        data["requester_id"] = user.id
        trade = Trade(**data)
        db.session.add(trade)
        db.session.flush()
        return trade

    @staticmethod
    def get_trades(user):
        trades = Trade.query.filter((user.id == Trade.requester_id) | (user.id == Trade.counterparty_id)).all()
        return trades

    @staticmethod
    def approve_trade(trade_id):
        Trade.query.filter_by(id=trade_id).update(dict(status=TradeStatus.approved))

    @staticmethod
    def change_traded_cards_ownership(trade_id):
        trade = get_trade(trade_id)

        # transfer cards from counterparty to requester
        cards_for_requester, requester_id = trade.counterparty_cards, trade.requester_id
        for card in cards_for_requester:
            Card.query.filter_by(id=card).update(
                dict(owner_id=requester_id, tradeable=False)
            )

        # transfer cards from requester to counterparty
        cards_for_counterparty, counterparty_id = (
            trade.requester_cards,
            trade.counterparty_id,
        )
        for card in cards_for_counterparty:
            Card.query.filter_by(id=card).update(
                dict(owner_id=counterparty_id, tradeable=False)
            )

        resp = {
            "id": trade_id,
            "status": TradeStatus.approved,
            "transferred_to_requester": cards_for_requester,
            "transferred_to_counterparty": cards_for_counterparty,
        }

        return resp

    @staticmethod
    def reject_trade(trade_id):
        Trade.query.filter_by(id=trade_id).update(dict(status=TradeStatus.rejected))
        resp = {"id": trade_id,
                "status": TradeStatus.rejected,
                "transferred_to_requester": [],
                "transferred_to_counterparty": [],
                }
        return resp
