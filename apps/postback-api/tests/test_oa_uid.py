"""Unit coverage for stable first-open oa_uid issuance."""

import os
import unittest
from uuid import UUID
from unittest.mock import patch

os.environ.setdefault("POSTGRES_USER", "postgres")
os.environ.setdefault("POSTGRES_DB", "postgres")
os.environ.setdefault("POSTGRES_PASSWORD", "postgres")
os.environ.setdefault("CLICKHOUSE_USER", "default")
os.environ.setdefault("CLICKHOUSE_PASSWORD", "password")

from api_app.oa_uid import issue_oa_uid_for_first_open, normalize_oa_uid_result


class TestIssueOaUidForFirstOpen(unittest.TestCase):
    """Verify issuance is stable across retries and insertion races."""

    @patch("api_app.oa_uid.insert_issued_oa_uid")
    @patch(
        "api_app.oa_uid.generate_oa_uid",
        return_value="1f8d66fe-4a2d-4da9-95e8-d54cdbaf4d6b",
    )
    @patch("api_app.oa_uid.query_issued_oa_uid", return_value=None)
    def test_creates_new_oa_uid_when_none_exists(
        self,
        query_mock,
        _generate_mock,
        insert_mock,
    ) -> None:
        """The first request inserts and returns a fresh oa_uid."""
        insert_mock.return_value = "1f8d66fe-4a2d-4da9-95e8-d54cdbaf4d6b"

        oa_uid = issue_oa_uid_for_first_open(
            event_uid="5730a99e-b009-41da-9d52-1315e26941c1",
            store_id="com.example.app",
            ifa="00000000-0000-0000-0000-000000000000",
        )

        self.assertEqual(oa_uid, "1f8d66fe-4a2d-4da9-95e8-d54cdbaf4d6b")
        insert_mock.assert_called_once()
        query_mock.assert_called_once()

    @patch("api_app.oa_uid.insert_issued_oa_uid")
    @patch("api_app.oa_uid.generate_oa_uid")
    @patch(
        "api_app.oa_uid.query_issued_oa_uid",
        return_value="3bd9e091-fa6e-4b91-8dd1-503f8d4fe8f2",
    )
    def test_reuses_existing_oa_uid_for_retried_first_open(
        self,
        query_mock,
        generate_mock,
        insert_mock,
    ) -> None:
        """A retried first app_open returns the original issued oa_uid."""
        oa_uid = issue_oa_uid_for_first_open(
            event_uid="5730a99e-b009-41da-9d52-1315e26941c1",
            store_id="com.example.app",
            ifa="00000000-0000-0000-0000-000000000000",
        )

        self.assertEqual(oa_uid, "3bd9e091-fa6e-4b91-8dd1-503f8d4fe8f2")
        generate_mock.assert_not_called()
        insert_mock.assert_not_called()
        query_mock.assert_called_once()

    @patch(
        "api_app.oa_uid.query_issued_oa_uid",
        side_effect=[
            None,
            "3bd9e091-fa6e-4b91-8dd1-503f8d4fe8f2",
        ],
    )
    @patch(
        "api_app.oa_uid.generate_oa_uid",
        return_value="1f8d66fe-4a2d-4da9-95e8-d54cdbaf4d6b",
    )
    @patch("api_app.oa_uid.insert_issued_oa_uid", return_value=None)
    def test_reuses_existing_oa_uid_after_insert_race(
        self,
        insert_mock,
        _generate_mock,
        query_mock,
    ) -> None:
        """If another request wins the insert race, return the stored oa_uid."""
        oa_uid = issue_oa_uid_for_first_open(
            event_uid="5730a99e-b009-41da-9d52-1315e26941c1",
            store_id="com.example.app",
            ifa="00000000-0000-0000-0000-000000000000",
        )

        self.assertEqual(oa_uid, "3bd9e091-fa6e-4b91-8dd1-503f8d4fe8f2")
        insert_mock.assert_called_once()
        self.assertEqual(query_mock.call_count, 2)


class TestNormalizeOaUidResult(unittest.TestCase):
    """Verify DB helper boundaries always normalize UUID values to strings."""

    def test_normalize_oa_uid_result_returns_none_for_none(self) -> None:
        """None should remain None."""
        self.assertIsNone(normalize_oa_uid_result(None))

    def test_normalize_oa_uid_result_converts_uuid_to_string(self) -> None:
        """UUID objects should be converted to string values."""
        result = normalize_oa_uid_result(
            UUID("3bd9e091-fa6e-4b91-8dd1-503f8d4fe8f2"),
        )
        self.assertEqual(result, "3bd9e091-fa6e-4b91-8dd1-503f8d4fe8f2")


if __name__ == "__main__":
    unittest.main()
