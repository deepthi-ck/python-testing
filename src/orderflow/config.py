from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration loaded from environment variables."""

    model_config = SettingsConfigDict(env_prefix="ORDERFLOW_", extra="ignore")

    app_name: str = "Orderflow Fulfillment"
    environment: str = "development"
    database_url: str = "sqlite:///./data/runtime/orderflow.db"
    api_key: str = Field(default="")
    api_key_header: str = "X-API-Key"
    max_line_items: int = 50
    max_quantity: int = 10_000
    min_quantity: int = 1
    free_shipping_threshold_cents: int = 10_000
    default_tax_bps: int = 800
    enable_sql_triggers: bool = True

    @property
    def sqlite_path(self) -> Path | None:
        if not self.database_url.startswith("sqlite"):
            return None
        if ":memory:" in self.database_url:
            return None
        raw = self.database_url.split("///", 1)[-1]
        return Path(raw)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
