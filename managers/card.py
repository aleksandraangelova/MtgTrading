import os
import uuid

from constants.common import TEMP_DIR
from db import db
from models.card import Card
from services.s3 import S3Service
from utils.common import decode_file


class CardManager:
    @staticmethod
    def create(data, user):
        data["owner_id"] = user.id
        extension = data.pop("extension")
        photo = data.pop("photo")
        file_name = f"{uuid.uuid4()}.{extension}"
        path = os.path.join(TEMP_DIR, file_name)
        decode_file(path, photo)
        s3 = S3Service()
        photo_url = s3.upload_photo(path, file_name)
        try:
            data["photo_url"] = photo_url
            card = Card(**data)
            db.session.add(card)
            db.session.flush()
            return card
        except Exception:
            s3.delete_photo(key=file_name)
        finally:
            os.remove(path)

    @staticmethod
    def get_cards_owned(uid):
        cards = Card.query.filter_by(owner_id=uid).all()
        return cards

    @staticmethod
    def get_cards_for_trade(uid):
        cards = (
            Card.query.filter(Card.tradeable == True).filter(Card.owner_id != uid).all()
        )
        return cards
