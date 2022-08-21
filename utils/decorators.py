from flask import request
from werkzeug.exceptions import BadRequest, Forbidden

from managers.auth import auth
from models import Trade
from models.enum import TradeStatus


def validate_schema(schema_name):
    def decorated_function(func):
        def wrapper(*args, **kwargs):
            data = request.get_json()
            schema = schema_name()
            errors = schema.validate(data)
            if not errors:
                return func(*args, **kwargs)
            raise BadRequest(errors)

        return wrapper

    return decorated_function


def validate_current_user_equals_param_uid():
    def decorated_function(func):
        def wrapper(*args, **kwargs):
            current_user = auth.current_user()
            if not current_user.id == kwargs["uid"]:
                raise Forbidden("Permission denied")
            return func(*args, **kwargs)

        return wrapper

    return decorated_function


def validate_current_user_can_see_trade_details():
    def decorated_function(func):
        def wrapper(*args, **kwargs):
            current_user = auth.current_user()
            data = Trade.query.filter(
                (Trade.requester_id == current_user.id)
                | (Trade.counterparty_id == current_user.id)
            ).first()
            if not data or current_user_is_not_trade_party(data, current_user.id):
                raise Forbidden("Permission denied")
            return func(*args, **kwargs)

        return wrapper

    return decorated_function


def validate_current_user_is_trade_counterparty():
    def decorated_function(func):
        def wrapper(*args, **kwargs):
            current_user = auth.current_user()
            trade_id = kwargs["trade_id"]

            data = Trade.query.filter(
                (Trade.id == trade_id)
                & (Trade.counterparty_id == current_user.id)
            ).first()

            if not data:
                raise Forbidden("Permission denied. You are not a counterparty to the trade.")
            return func(*args, **kwargs)
        return wrapper
    return decorated_function


def validate_trade_status():
    def decorated_function(func):
        def wrapper(*args, **kwargs):
            trade_id = kwargs["trade_id"]
            trade = Trade.query.filter(
                (Trade.id == trade_id)
            ).first()

            if trade.status != TradeStatus.pending:
                raise Forbidden("Permission denied. You can only approve or reject a pending trade.")
            return func(*args, **kwargs)
        return wrapper
    return decorated_function


def current_user_is_not_trade_party(trade: Trade, uid):
    return trade.requester_id != uid and trade.counterparty_id != uid
