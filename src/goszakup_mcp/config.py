"""Runtime configuration read from environment variables. The token never lives in code."""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Literal

DataSource = Literal["mock", "ows"]


@dataclass(frozen=True, slots=True)
class Settings:
    source: DataSource
    token: str | None

    @property
    def has_token(self) -> bool:
        return bool(self.token)


def load_settings(env: dict[str, str] | None = None) -> Settings:
    """Build settings from the environment.

    GOSZAKUP_SOURCE: "mock" (default) or "ows" (official API, needs GOSZAKUP_TOKEN).
    """
    env = dict(os.environ) if env is None else env
    raw_source = env.get("GOSZAKUP_SOURCE", "mock").strip().lower()
    if raw_source not in ("mock", "ows"):
        raise ValueError(f"GOSZAKUP_SOURCE must be 'mock' or 'ows', got {raw_source!r}")
    token = env.get("GOSZAKUP_TOKEN") or None
    if raw_source == "ows" and not token:
        raise ValueError("GOSZAKUP_SOURCE=ows requires GOSZAKUP_TOKEN")
    source: DataSource = "ows" if raw_source == "ows" else "mock"
    return Settings(source=source, token=token)
