from .db import Base, SessionLocal, engine
from .models import RemovalRequest


def main():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        providers = ["alpha", "beta", "gamma"]
        for i in range(60):
            db.add(
                RemovalRequest(
                    email=f"candidate-user-{i}@example.com",
                    provider=providers[i % len(providers)],
                    status="pending" if i % 4 else "completed",
                    attempts=0,
                )
            )
        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    main()
