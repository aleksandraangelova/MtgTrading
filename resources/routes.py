from resources.auth import RegisterResource, LoginResource
from resources.card import CardResource
from resources.trade import TradeResource, TradeDetailsResource
from resources.trader import TraderCardsResource

routes = (
    (RegisterResource, "/register/"),
    (LoginResource, "/login/"),
    (CardResource, "/card/"),
    (TraderCardsResource, "/trader/<int:uid>/cards/"),
    (TradeResource, "/trade/"),
    (TradeDetailsResource, "/trade/<int:trade_id>/details"),
)
