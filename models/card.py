from db import db
from models.enum import CardCondition


class Card(db.Model):
    __tablename__ = "card"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    set = db.Column(db.String(50), nullable=False)
    foil = db.Column(db.Boolean(), nullable=False)
    condition = db.Column(db.Enum(CardCondition), nullable=False)
    photo_url = db.Column(db.String(255), nullable=False)
    owner_id = db.Column(db.Integer(), db.ForeignKey("trader.id"), nullable=False)
    tradeable = db.Column(db.Boolean(), nullable=False)
