"""Helpers for issuing stable oa_uid values on first app_open."""

from api_app.tools import generate_oa_uid


def normalize_oa_uid_result(result: object | None) -> str | None:
    """Normalize persisted oa_uid values to strings at the boundary."""
    return None if result is None else str(result)


def query_issued_oa_uid(event_uid: str) -> str | None:
    """Return any oa_uid already issued for this event uid."""
    from dbcon.queries import query_oa_uid_issuance

    return query_oa_uid_issuance(event_uid=event_uid)


def insert_issued_oa_uid(
    event_uid: str,
    oa_uid: str,
    store_id: str,
    ifa: str,
) -> str | None:
    """Persist a newly issued oa_uid, unless another request won the race."""
    from dbcon.queries import insert_oa_uid_issuance

    return insert_oa_uid_issuance(
        event_uid=event_uid,
        oa_uid=oa_uid,
        store_id=store_id,
        ifa=ifa,
    )


def issue_oa_uid_for_first_open(event_uid: str, store_id: str, ifa: str) -> str:
    """Issue or reuse an oa_uid for a first app_open request."""
    existing_oa_uid = query_issued_oa_uid(event_uid=event_uid)
    if existing_oa_uid is not None:
        return existing_oa_uid

    new_oa_uid = generate_oa_uid()
    inserted_oa_uid = insert_issued_oa_uid(
        event_uid=event_uid,
        oa_uid=new_oa_uid,
        store_id=store_id,
        ifa=ifa,
    )
    if inserted_oa_uid is not None:
        return inserted_oa_uid

    existing_oa_uid = query_issued_oa_uid(event_uid=event_uid)
    if existing_oa_uid is None:
        msg = f"Unable to issue oa_uid for first app_open {event_uid=}"
        raise ValueError(msg)
    return existing_oa_uid
