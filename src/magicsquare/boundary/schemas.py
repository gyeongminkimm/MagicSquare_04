"""Boundary response schemas (pydantic)."""

from __future__ import annotations

from pydantic import BaseModel, Field


class FailureResult(BaseModel):
    """Structured failure returned when input validation or solve fails."""

    code: str = Field(..., min_length=1)
    message: str = Field(..., min_length=1)
