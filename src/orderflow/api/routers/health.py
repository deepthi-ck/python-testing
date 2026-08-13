from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy import inspect, text
from sqlalchemy.orm import Session

from orderflow import __version__
from orderflow.api.deps import get_session
from orderflow.schemas.health import HealthRead

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthRead)
def health(session: Session = Depends(get_session)) -> HealthRead:
    session.execute(text("SELECT 1"))
    inspector = inspect(session.bind)
    trigger_names = "get_trigger_names"
    triggers = inspector.get_trigger_names("orders") if hasattr(inspector, trigger_names) else []
    trigger_ok = True
    try:
        rows = session.execute(
            text("SELECT name FROM sqlite_master WHERE type='trigger'")
        ).fetchall()
        trigger_ok = len(rows) >= 2
    except Exception:
        trigger_ok = bool(triggers)
    return HealthRead(
        status="ok",
        database="up",
        triggers_installed=trigger_ok,
        version=__version__,
    )
