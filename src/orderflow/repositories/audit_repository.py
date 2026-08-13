from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from orderflow.models.audit import AuditEvent


class AuditRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def list_for_entity(
        self, entity_type: str, entity_id: int, limit: int = 50
    ) -> list[AuditEvent]:
        statement = (
            select(AuditEvent)
            .where(AuditEvent.entity_type == entity_type, AuditEvent.entity_id == entity_id)
            .order_by(AuditEvent.id.desc())
            .limit(limit)
        )
        return list(self._session.scalars(statement))

    def count_all(self) -> int:
        return int(self._session.scalar(select(func.count(AuditEvent.id))) or 0)
