"""Shared tools to standardize enriching postbacks."""

import datetime
import uuid

from litestar import Request

EMPTY_IFA = "00000000-0000-0000-0000-000000000000"


def generate_link_uid() -> str:
    """Generate a random link uid."""
    return str(uuid.uuid4())


def is_valid_ifa(ifa: str | None) -> bool:
    """Check if a string is a valid ifa."""
    if ifa is None:
        return False
    try:
        uuid_obj = uuid.UUID(ifa)
        return (
            uuid_obj.version == 4  # noqa: PLR2004
            and str(uuid_obj) == ifa.lower()
        ) or ifa == EMPTY_IFA
    except ValueError:
        return False


def is_valid_uuid(val: str) -> bool:
    """Check if a string is a valid UUID."""
    try:
        uuid_obj = uuid.UUID(val)
        return (
            uuid_obj.version == 4  # noqa: PLR2004
            and str(uuid_obj) == val.lower()
        )
    except ValueError:
        return False


def now() -> str:
    """Return datetime in epoch milliseconds as integer."""
    timestamp_with_ms_int = str(
        int(datetime.datetime.now(datetime.UTC).timestamp() * 1000),
    )
    return timestamp_with_ms_int


def get_client_ip(request: Request) -> str:
    """

    Get the real client IP, checking X-Forwarded-For header first.

    If the X-Forwarded-For header is not present, return the client host.

    Todo: This will need to be tested.

    """
    forwarded_for = request.headers.get("X-Forwarded-For")
    ip_host: str = request.client.host
    if forwarded_for:
        # Get the first IP in the chain
        ip_str: str = forwarded_for.split(",")[0].strip()
        return ip_str
    return ip_host
