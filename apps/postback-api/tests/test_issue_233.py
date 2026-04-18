"""Regression coverage for server-side oa_uid issuance on first app_open."""

import os
import unittest
from unittest.mock import Mock, patch
from uuid import UUID

os.environ.setdefault("POSTGRES_USER", "postgres")
os.environ.setdefault("POSTGRES_DB", "postgres")
os.environ.setdefault("POSTGRES_PASSWORD", "postgres")
os.environ.setdefault("CLICKHOUSE_USER", "default")
os.environ.setdefault("CLICKHOUSE_PASSWORD", "password")

from litestar import Litestar
from litestar.testing import TestClient

from api_app.controllers.postbacks import PostbackController


class TestServerIssuedOaUid(unittest.TestCase):
    """Focused API coverage for issue #233."""

    def make_client(self) -> TestClient[Litestar]:
        """Build a lightweight app with only the postback controller under test."""
        app = Litestar(route_handlers=[PostbackController], debug=True)
        return TestClient(app=app)

    @patch(
        "api_app.controllers.postbacks.get_geo",
        return_value={"country_iso": "", "state_iso": "", "city_name": ""},
    )
    @patch(
        "api_app.controllers.postbacks.issue_oa_uid_for_first_open",
        return_value="3bd9e091-fa6e-4b91-8dd1-503f8d4fe8f2",
    )
    @patch("api_app.controllers.postbacks.to_kafka")
    def test_first_app_open_without_oa_uid_returns_server_generated_id(
        self,
        to_kafka_mock: Mock,
        issue_oa_uid_mock: Mock,
        _get_geo_mock: Mock,
    ) -> None:
        """The first app_open may omit oa_uid and receive one from the server."""
        payload = {
            "event_id": "app_open",
            "event_time": 1732003510046,
            "event_uid": "5730a99e-b009-41da-9d52-1315e26941c1",
            "ifa": "00000000-0000-0000-0000-000000000000",
        }

        with self.make_client() as client:
            response = client.post("/collect/events/com.example.app", json=payload)

        self.assertEqual(response.status_code, 201)
        body = response.json()
        self.assertIn("oa_uid", body)
        self.assertEqual(str(UUID(body["oa_uid"])), body["oa_uid"])
        issue_oa_uid_mock.assert_called_once_with(
            event_uid=payload["event_uid"],
            store_id="com.example.app",
            ifa=payload["ifa"],
        )
        event_data, topic = to_kafka_mock.call_args.args
        self.assertEqual(topic, "events")
        self.assertEqual(event_data.oa_uid, body["oa_uid"])
        self.assertEqual(event_data.event_id, "app_open")

    @patch(
        "api_app.controllers.postbacks.get_geo",
        return_value={"country_iso": "", "state_iso": "", "city_name": ""},
    )
    @patch("api_app.controllers.postbacks.to_kafka")
    def test_existing_client_supplied_oa_uid_still_works(
        self,
        to_kafka_mock: Mock,
        _get_geo_mock: Mock,
    ) -> None:
        """Existing clients that already send oa_uid should remain compatible."""
        payload = {
            "event_id": "tutorial",
            "event_time": 1732003510046,
            "event_uid": "5730a99e-b009-41da-9d52-1315e26941c1",
            "oa_uid": "3bd9e091-fa6e-4b91-8dd1-503f8d4fe8f2",
            "ifa": "00000000-0000-0000-0000-000000000000",
        }

        with self.make_client() as client:
            response = client.post("/collect/events/com.example.app", json=payload)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json(),
            {"oa_uid": "3bd9e091-fa6e-4b91-8dd1-503f8d4fe8f2"},
        )
        event_data, topic = to_kafka_mock.call_args.args
        self.assertEqual(topic, "events")
        self.assertEqual(event_data.oa_uid, payload["oa_uid"])
        self.assertEqual(event_data.event_id, "tutorial")

    def test_non_app_open_without_oa_uid_is_rejected(self) -> None:
        """Only the first app_open may rely on server-side issuance."""
        payload = {
            "event_id": "tutorial",
            "event_time": 1732003510046,
            "event_uid": "5730a99e-b009-41da-9d52-1315e26941c1",
            "ifa": "00000000-0000-0000-0000-000000000000",
        }

        with self.make_client() as client:
            response = client.post("/collect/events/com.example.app", json=payload)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()["detail"],
            "Missing oa_uid, only first app_open may omit it",
        )


if __name__ == "__main__":
    unittest.main()
