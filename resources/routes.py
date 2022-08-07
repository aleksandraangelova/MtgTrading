from resources.auth import RegisterResource, LoginResource
from resources.card import CardResource

routes = (
    (RegisterResource, "/register/"),
    (LoginResource, "/login/"),
    (CardResource, "/card/"),
)
