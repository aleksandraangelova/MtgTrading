from db import db
from models.enum import TradeStatus


class Trade:
    __tablename__ = "trade"

    id = db.Column(db.Integer, primary_key=True)
    requester_id = db.Column(
        db.Integer(), db.ForeignKey("trader.id"), nullable=False
    )
    requester_cards = db.Column(db.ARRAY(db.Integer), nullable=False)
    counterparty_id = db.Column(
        db.Integer(), db.ForeignKey("trader.id"), nullable=False
    )
    counterparty_cards = db.Column(db.ARRAY(db.Integer), nullable=False)
    status = db.Column(db.Enum(TradeStatus), default=TradeStatus.pending, nullable=False)
