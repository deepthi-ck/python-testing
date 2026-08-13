from __future__ import annotations

from collections.abc import Generator
from pathlib import Path

from sqlalchemy import create_engine, event, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
from sqlalchemy.pool import StaticPool

from orderflow.config import Settings, get_settings

AUDIT_TRIGGERS = (
    """
    CREATE TRIGGER IF NOT EXISTS trg_orders_after_insert
    AFTER INSERT ON orders
    BEGIN
        INSERT INTO audit_events (entity_type, entity_id, action, payload, created_at)
        VALUES (
            'order',
            NEW.id,
            'INSERT',
            json_object(
                'status', NEW.status,
                'total_cents', NEW.total_cents,
                'customer_id', NEW.customer_id
            ),
            CURRENT_TIMESTAMP
        );
    END;
    """,
    """
    CREATE TRIGGER IF NOT EXISTS trg_orders_after_update
    AFTER UPDATE ON orders
    BEGIN
        INSERT INTO audit_events (entity_type, entity_id, action, payload, created_at)
        VALUES (
            'order',
            NEW.id,
            'UPDATE',
            json_object(
                'old_status', OLD.status,
                'new_status', NEW.status,
                'old_total_cents', OLD.total_cents,
                'new_total_cents', NEW.total_cents
            ),
            CURRENT_TIMESTAMP
        );
    END;
    """,
    """
    CREATE TRIGGER IF NOT EXISTS trg_inventory_after_update
    AFTER UPDATE ON inventory_lots
    BEGIN
        INSERT INTO audit_events (entity_type, entity_id, action, payload, created_at)
        VALUES (
            'inventory',
            NEW.id,
            'UPDATE',
            json_object(
                'sku', NEW.sku,
                'old_on_hand', OLD.on_hand,
                'new_on_hand', NEW.on_hand,
                'old_reserved', OLD.reserved,
                'new_reserved', NEW.reserved
            ),
            CURRENT_TIMESTAMP
        );
    END;
    """,
)


class Base(DeclarativeBase):
    pass


def _configure_sqlite(engine: Engine) -> None:
    @event.listens_for(engine, "connect")
    def _set_sqlite_pragma(dbapi_connection, _connection_record) -> None:
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.execute("PRAGMA journal_mode=WAL")
        cursor.close()


def create_db_engine(settings: Settings | None = None) -> Engine:
    settings = settings or get_settings()
    sqlite_path = settings.sqlite_path
    if sqlite_path is not None:
        sqlite_path.parent.mkdir(parents=True, exist_ok=True)
    connect_args = {}
    if settings.database_url.startswith("sqlite"):
        connect_args = {"check_same_thread": False}
    engine_kwargs: dict[str, object] = {"echo": False, "future": True, "connect_args": connect_args}
    if settings.database_url.endswith(":memory:"):
        engine_kwargs["poolclass"] = StaticPool
    engine = create_engine(settings.database_url, **engine_kwargs)
    if settings.database_url.startswith("sqlite"):
        _configure_sqlite(engine)
    return engine


def install_triggers(engine: Engine) -> None:
    if not get_settings().enable_sql_triggers:
        return
    with engine.begin() as connection:
        for statement in AUDIT_TRIGGERS:
            connection.execute(text(statement))


def create_session_factory(engine: Engine) -> sessionmaker[Session]:
    return sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False,
        future=True,
    )


def session_scope(factory: sessionmaker[Session]) -> Generator[Session, None, None]:
    session = factory()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def ensure_runtime_dir() -> Path:
    path = Path("data/runtime")
    path.mkdir(parents=True, exist_ok=True)
    return path
