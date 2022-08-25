from unittest.mock import patch

from flask_testing import TestCase

from config import create_app
from db import db
from models import TraderModel, Card
from models.trade import Trade
from services.aws_ses import SESService
from tests.helpers import get_headers_with_authorization_and_user, encoded_photo, \
    encoded_photo_extension


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

    @patch.object(SESService, "send_email")
    def test_create_trade_success(self, mocked_ses):
        # Prerequisites for creating a trade: counterparties exist and have cards
        self.headers_1, self.user_1 = get_headers_with_authorization_and_user()
        self.headers_2, self.user_2 = get_headers_with_authorization_and_user()
        # Add card to User 1
        card_1 = {
        "set": "First Set",
        "tradeable": True,
        "foil": False,
        "name": "Test Card 1",
        "condition": "mint",
        "photo": encoded_photo,
        "extension": encoded_photo_extension
        }
        self.client.post("/card/", headers=self.headers_1, json=card_1)
        # Add card to User 2
        card_2 = {
        "set": "Second Set",
        "tradeable": True,
        "foil": False,
        "name": "Test Card 2",
        "condition": "mint",
        "photo": encoded_photo,
        "extension": encoded_photo_extension
        }
        self.client.post("/card/", headers=self.headers_2, json=card_2)

        # traders are 3 because we already created one for the first test
        assert len(TraderModel.query.all()) == 3
        assert len(Card.query.all()) == 2

        trades = Trade.query.all()
        assert len(trades) == 0
        data = {"requester_cards": [1], "counterparty_id": 1, "counterparty_cards": [2]}
        resp = self.client.post(self.url, headers=self.headers_1, json=data)
        trades = Trade.query.all()
        assert len(trades) == 1
        assert resp.status_code == 201


