from werkzeug.exceptions import BadRequest
from werkzeug.security import generate_password_hash, check_password_hash

from db import db
from managers.auth import AuthManager
from models.user import TraderModel


class TraderManager:
    @staticmethod
    def register(trader_data):
        trader_data["password"] = generate_password_hash(trader_data["password"])
        user = TraderModel(**trader_data)
        db.session.add(user)
        return AuthManager.encode_token(user)

    @staticmethod
    def login(login_data):
        complainer = TraderModel.query.filter_by(email=login_data["email"]).first()
        if not complainer:
            raise BadRequest("No such email! Please register!")

        if check_password_hash(complainer.password, login_data["password"]):
            return AuthManager.encode_token(complainer)
        raise BadRequest("Wrong credentials!")