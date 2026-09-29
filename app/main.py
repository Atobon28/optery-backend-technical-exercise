from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from .db import Base, engine, get_db
from .models import RemovalRequest
from .service import create_removal_request, list_requests_with_summary, process_removal_request

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Removal Requests Exercise")


class RemovalRequestCreate(BaseModel):
    email: EmailStr
    provider: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/removal-requests")
def create(payload: RemovalRequestCreate, db: Session = Depends(get_db)):
    item = create_removal_request(db, payload.email, payload.provider)
    return {
        "id": item.id,
        "email": item.email,
        "provider": item.provider,
        "status": item.status,
    }


@app.post("/removal-requests/{request_id}/process")
def process(request_id: int, db: Session = Depends(get_db)):
    try:
        item = process_removal_request(db, request_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    return {
        "id": item.id,
        "status": item.status,
        "attempts": item.attempts,
        "external_reference": item.external_reference,
    }


@app.get("/removal-requests/{request_id}")
def get_one(request_id: int, db: Session = Depends(get_db)):
    item = db.get(RemovalRequest, request_id)
    if item is None:
        raise HTTPException(status_code=404, detail="request not found")
    return {
        "id": item.id,
        "email": item.email,
        "provider": item.provider,
        "status": item.status,
        "attempts": item.attempts,
        "external_reference": item.external_reference,
    }


@app.get("/removal-requests")
def list_all(db: Session = Depends(get_db)):
    return list_requests_with_summary(db)
