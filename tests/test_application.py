from flask_testing import TestCase

from config import create_app
from db import db
from tests.helpers import generate_token

ENDPOINTS_DATA = (
    ("/card/", "POST"),
    ("/trader/1/cards/", "GET"),
    ("/trade/", "POST"),
    ("/trade/", "GET"),
    ("/trade/1/", "GET"),
    ("/trade/1/", "DELETE"),
    ("/trade/1/approve/", "PUT"),
    ("/trade/1/reject/", "PUT"),
    ("/cards/tradeable", "GET"),
)


class TestApp(TestCase):
    def create_app(self):
        return create_app("config.TestConfig")

    def setUp(self):
        db.init_app(self.app)
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def iterate_endpoints(
        self,
        endpoints_data,
        status_code_method,
        expected_resp_body,
        headers=None,
        payload=None,
    ):
        if not headers:
            headers = {}
        if not payload:
            payload = {}
        resp = None
        for url, method in endpoints_data:
            if method == "GET":
                resp = self.client.get(url, headers=headers)
            elif method == "POST":
                resp = self.client.post(url, headers=headers)
            elif method == "PUT":
                resp = self.client.put(url, headers=headers)
            elif method == "DELETE":
                resp = self.client.delete(url, headers=headers)
            status_code_method(resp)
            self.assertEqual(resp.json, expected_resp_body)

    def test_login_required(self):
        self.iterate_endpoints(
            ENDPOINTS_DATA, self.assert_401, {"message": "Missing token"}
        )

    def test_invalid_token_raises(self):
        headers = {"Authorization": "Bearer eyJ0eX"}
        self.iterate_endpoints(
            ENDPOINTS_DATA, self.assert_401, {"message": "Invalid token"}, headers
        )
