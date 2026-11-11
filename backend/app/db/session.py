from collections.abc import Generator
from pathlib import Path

from sqlalchemy import Engine, create_engine, event
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings
from app.db.base import enable_sqlite_foreign_keys


def _ensure_sqlite_directory(url: str) -> None:
    path = url.removeprefix("sqlite:///")
    if path and path != ":memory:":
        parent = Path(path).parent
        if str(parent):
            parent.mkdir(parents=True, exist_ok=True)


def _create_engine() -> Engine:
    connect_args = {}
    if settings.DATABASE_URL.startswith("sqlite"):
        _ensure_sqlite_directory(settings.DATABASE_URL)
        connect_args = {"check_same_thread": False}
    return create_engine(settings.DATABASE_URL, connect_args=connect_args)


event.listen(Engine, "connect", enable_sqlite_foreign_keys)

engine = _create_engine()
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
