from resources.auth import RegisterResource, LoginResource
from resources.card import CardResource, CardsTradeableResource
from resources.trade import TradeResource, TradeDetailsResource, ApproveTradeResource, RejectTradeResource
from resources.trader import TraderCardsResource

routes = (
    (RegisterResource, "/register/"),
    (LoginResource, "/login/"),
    (CardResource, "/card/"),
    (TraderCardsResource, "/trader/<int:uid>/cards/"),
    (TradeResource, "/trade/"),
    (TradeDetailsResource, "/trade/<int:trade_id>/details/"),
    (ApproveTradeResource, "/trade/<int:trade_id>/approve/"),
    (RejectTradeResource, "/trade/<int:trade_id>/reject/"),
    (CardsTradeableResource, "/cards/tradeable")
)
