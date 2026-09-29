from datetime import datetime

from sqlalchemy.orm import Session

from .models import RemovalRequest
from .provider import provider_client


def create_removal_request(db: Session, email: str, provider: str) -> RemovalRequest:
    item = RemovalRequest(email=email, provider=provider, status="pending")
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def process_removal_request(db: Session, request_id: int) -> RemovalRequest:
    """
    Intentionally flawed workflow for the live exercise.

    The code works in the happy path, but has production reliability and
    concurrency problems that the candidate should discover and address.
    """
    item = db.get(RemovalRequest, request_id)
    if item is None:
        raise ValueError("request not found")

    if item.status == "completed":
        return item

    # BUG: read/check/update is not protected from concurrent workers.
    item.status = "processing"
    item.attempts += 1
    item.updated_at = datetime.utcnow()
    db.commit()

    # BUG: external side effect happens before durable confirmation.
    # If the process dies after this call, a retry can duplicate the action.
    external_reference = provider_client.remove(item.email, item.provider)

    item.external_reference = external_reference
    item.status = "completed"
    item.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(item)
    return item


def list_requests_with_summary(db: Session) -> list[dict]:
    """Intentionally inefficient implementation for performance debugging."""
    rows = db.query(RemovalRequest).order_by(RemovalRequest.created_at.desc()).all()
    result: list[dict] = []

    for row in rows:
        # BUG: repeated full-table query inside the loop.
        same_provider_count = (
            db.query(RemovalRequest)
            .filter(RemovalRequest.provider == row.provider)
            .count()
        )
        result.append(
            {
                "id": row.id,
                "email": row.email,
                "provider": row.provider,
                "status": row.status,
                "attempts": row.attempts,
                "same_provider_count": same_provider_count,
            }
        )

    return result
