from app.db import Base, SessionLocal, engine
from app.models import RemovalRequest
from app.provider import provider_client
from app.service import create_removal_request, process_removal_request


def setup_function():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    provider_client.calls.clear()


def test_create_and_process_happy_path():
    db = SessionLocal()
    try:
        item = create_removal_request(db, "person@example.com", "alpha")
        result = process_removal_request(db, item.id)
        assert result.status == "completed"
        assert result.attempts == 1
        assert result.external_reference is not None
        assert len(provider_client.calls) == 1
    finally:
        db.close()


def test_completed_request_is_not_processed_again():
    db = SessionLocal()
    try:
        item = RemovalRequest(
            email="done@example.com",
            provider="alpha",
            status="completed",
            attempts=1,
            external_reference="ext-existing",
        )
        db.add(item)
        db.commit()
        db.refresh(item)

        result = process_removal_request(db, item.id)
        assert result.external_reference == "ext-existing"
        assert len(provider_client.calls) == 0
    finally:
        db.close()
