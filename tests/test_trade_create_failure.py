from unittest.mock import patch

from flask_testing import TestCase

from config import create_app
from db import db
from models import Card, TraderModel
from models.trade import Trade
from services.aws_ses import SESService
from services.s3 import S3Service
from tests.helpers import (encoded_photo, encoded_photo_extension,
                           get_headers_with_authorization_and_user)


class TestTrade(TestCase):
    url = "/trade/"

    def create_app(self):
        return create_app("config.TestConfig")

    def setUp(self):
        db.init_app(self.app)
        db.create_all()
        self.headers, user = get_headers_with_authorization_and_user()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_trade_schema_missing_fields_raises(self):
        trades = Trade.query.all()
        assert len(trades) == 0
        data = {}
        resp = self.client.post(self.url, headers=self.headers, json=data)
        self.assert400(resp)

        assert resp.json["message"] == {
            "counterparty_cards": ["Missing data for required field."],
            "counterparty_id": ["Missing data for required field."],
            "requester_cards": ["Missing data for required field."],
        }

        trades = Trade.query.all()
        assert len(trades) == 0