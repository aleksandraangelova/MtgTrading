import os
from unittest.mock import patch

from flask_testing import TestCase

from config import create_app
from constants.common import TEMP_DIR
from db import db
from managers.card import CardManager
from models import Card, CardCondition
from services.s3 import S3Service
from tests.factories import TraderFactory
from tests.helpers import (
    encoded_photo,
    encoded_photo_extension,
    generate_token,
    mock_uuid,
)


class TestComplaint(TestCase):
    url = "/card/"

    def create_app(self):
        return create_app("config.TestConfig")

    def setUp(self):
        db.init_app(self.app)
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_complaint_schema_missing_fields_raises(self):
        cards = Card.query.all()
        assert len(cards) == 0

        user = TraderFactory()
        token = generate_token(user)
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        data = {}
        resp = self.client.post(self.url, headers=headers, json=data)
        self.assert400(resp)

        assert resp.json["message"] == {'condition': ['Missing data for required field.'],
                                        'extension': ['Missing data for required field.'],
                                        'foil': ['Missing data for required field.'],
                                        'name': ['Missing data for required field.'],
                                        'photo': ['Missing data for required field.'],
                                        'set': ['Missing data for required field.'],
                                        'tradeable': ['Missing data for required field.']}

        cards = Card.query.all()
        assert len(cards) == 0

    @patch("uuid.uuid4", mock_uuid)
    @patch.object(S3Service, "upload_photo", return_value="some.s3.url")
    def test_create_card(self, mocked_s3):
        cards = Card.query.all()
        assert len(cards) == 0

        trader = TraderFactory()
        token = generate_token(trader)
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        data = {
            "name": "Test Title",
            "set": "Test Set",
            "condition": CardCondition.good.name,
            "tradeable": False,
            "foil": True,
            "photo": encoded_photo,
            "extension": encoded_photo_extension,
        }
        resp = self.client.post(self.url, headers=headers, json=data)
        assert resp.status_code == 201
        resp = resp.json
        expected_resp = {
            "name": data["name"],
            "set": data["set"],
            "condition": data["condition"],
            "tradeable": data["tradeable"],
            "foil": data["foil"]
        }
        assert resp == expected_resp

        file_name = f"{str(mock_uuid())}.{encoded_photo_extension}"
        path = os.path.join(TEMP_DIR, file_name)

        mocked_s3.assert_called_once_with(path, file_name)

        # Test DB
        cards = Card.query.all()
        assert len(cards) == 1

        # # Can build what we expect in the record
        # assert dict(complaints[0]) == {""}

    def test_register_schema_raises_invalid_first_name(self):
        data = {
            "last_name": "test",
            "city": "Sofia",
            "email": "test@test.com",
            "password": "123@456asd1"
        }
        url = "/register/"
        headers = {"Content-Type": "application/json"}

        # Missing name
        resp = self.client.post(url, headers=headers, json=data)
        self.assert400(resp)
        assert resp.json == {"message": {"first_name": ["Missing data for required field."]}}

        # Too short first name
        data["first_name"] = "A"
        resp = self.client.post(url, headers=headers, json=data)
        self.assert400(resp)
        assert resp.json == {"message": {"first_name": ["Length must be between 2 and 20."]}}

        # Too long first name
        data["first_name"] = "AAAAAAAAAAAAAAAAAAAAAA"
        resp = self.client.post(url, headers=headers, json=data)
        self.assert400(resp)
        assert resp.json == {"message": {"first_name": ["Length must be between 2 and 20."]}}