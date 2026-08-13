from __future__ import annotations

from pydantic import BaseModel


class HealthRead(BaseModel):
    status: str
    database: str
    triggers_installed: bool
    version: str
