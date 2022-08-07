from sqlalchemy import func

from db import db
from models.enum import TradeStatus


class Trade(db.Model):
    __tablename__ = "trade"

    id = db.Column(db.Integer, primary_key=True)
    created_on = db.Column(db.DateTime, nullable=False, server_default=func.now())
    status = db.Column(db.Enum(TradeStatus), default=TradeStatus.pending, nullable=False)