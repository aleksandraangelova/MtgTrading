from resources.auth import RegisterResource, LoginResource
from resources.card import CardResource, CardsTradeableResource
from resources.trade import TradeCreateResource, TradeResource, ApproveTradeResource, RejectTradeResource
from resources.trader import TraderCardsResource

routes = (
    (RegisterResource, "/register/"),
    (LoginResource, "/login/"),
    (CardResource, "/card/"),
    (TraderCardsResource, "/trader/<int:uid>/cards/"),
    (TradeCreateResource, "/trade/"),
    (TradeResource, "/trade/<int:trade_id>"),
    (ApproveTradeResource, "/trade/<int:trade_id>/approve/"),
    (RejectTradeResource, "/trade/<int:trade_id>/reject/"),
    (CardsTradeableResource, "/cards/tradeable")
)
