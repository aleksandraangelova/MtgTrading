from sqlalchemy import func

from db import db
from models.enum import TradeStatus


class Trade(db.Model):
    __tablename__ = "trade"

    id = db.Column(db.Integer, primary_key=True)
    created_on = db.Column(db.DateTime, nullable=False, server_default=func.now())
    requester_id = db.Column(db.Integer(), db.ForeignKey("trader.id"), nullable=False)
    requester_cards = db.Column(db.ARRAY(db.Integer), nullable=False)
    counterparty_id = db.Column(
        db.Integer(), db.ForeignKey("trader.id"), nullable=False
    )
    counterparty_cards = db.Column(db.ARRAY(db.Integer), nullable=False)
    status = db.Column(
        db.Enum(TradeStatus), default=TradeStatus.pending, nullable=False
    )