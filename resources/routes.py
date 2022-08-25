from resources.auth import LoginResource, RegisterResource
from resources.card import CardResource, CardsTradeableResource
from resources.trade import (ApproveTradeResource, RejectTradeResource,
                             TradeCreateResource, TradeResource)
from resources.trader import TraderCardsResource

routes = (
    (RegisterResource, "/register/"),
    (LoginResource, "/login/"),
    (CardResource, "/card/"),
    (TraderCardsResource, "/trader/<int:uid>/cards/"),
    (TradeCreateResource, "/trade/"),
    (TradeResource, "/trade/<int:trade_id>/"),
    (ApproveTradeResource, "/trade/<int:trade_id>/approve/"),
    (RejectTradeResource, "/trade/<int:trade_id>/reject/"),
    (CardsTradeableResource, "/cards/tradeable"),
)
