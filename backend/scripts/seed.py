from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import generate_api_key, hash_api_key
from app.db.session import SessionLocal
from app.models import User, Vehicle

VEHICLES = [
    {"plate": "ABC123", "name": "Camión 01", "alpha_id": "ALP-001", "beta_code": None},
    {"plate": "DEF456", "name": "Camión 02", "alpha_id": "ALP-002", "beta_code": None},
    {"plate": "GHI789", "name": "Camión 03", "alpha_id": None, "beta_code": "BT-9001"},
    {"plate": "JKL012", "name": "Camión 04", "alpha_id": "ALP-004", "beta_code": "BT-9004"},
]


def seed_vehicles(db: Session) -> None:
    existing_plates = set(db.scalars(select(Vehicle.plate)).all())
    for data in VEHICLES:
        if data["plate"] not in existing_plates:
            db.add(Vehicle(**data))
    db.commit()


def seed_user(db: Session) -> None:
    if db.scalar(select(User).where(User.name == "Simulator")) is not None:
        return

    raw_key = settings.SEED_API_KEY or generate_api_key()
    if settings.SEED_API_KEY is None:
        print(f"Generated API key for Simulator: {raw_key}")
    db.add(User(name="Simulator", api_key_hash=hash_api_key(raw_key)))
    db.commit()


def main() -> None:
    with SessionLocal() as db:
        seed_vehicles(db)
        seed_user(db)


if __name__ == "__main__":
    main()
