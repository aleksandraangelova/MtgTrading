import enum


class UserRole(enum.Enum):
    trader = "Trader"
    admin = "Admin"


class CardCondition(enum.Enum):
    mint = "Mint"
    excellent = "Excellent"
    good = "Good"
    played = "Played"
    poor = "Poor"


class TradeStatus(enum.Enum):
    pending = "Pending"
    approved = "Approved"
    rejected = "Rejected"
