import sqlite3

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


def enable_sqlite_foreign_keys(dbapi_connection, _connection_record) -> None:
    """Enable FK enforcement on SQLite connections (off by default)."""
    if isinstance(dbapi_connection, sqlite3.Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()
