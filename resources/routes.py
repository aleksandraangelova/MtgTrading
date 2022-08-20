from resources.auth import RegisterResource, LoginResource
from resources.card import CardResource
from resources.trader import TraderCardsResource

routes = (
    (RegisterResource, "/register/"),
    (LoginResource, "/login/"),
    (CardResource, "/card/"),
    (TraderCardsResource, "/trader/<int:uid>/cards/")
)
