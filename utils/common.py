import base64

from models import Trade


def decode_file(path, encoded_file):
    with open(path, "wb") as f:
        f.write(base64.b64decode(encoded_file.encode("utf-8")))


def get_trade(trade_id):
    return Trade.query.filter_by(id=trade_id).first()
