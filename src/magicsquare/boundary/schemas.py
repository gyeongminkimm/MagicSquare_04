"""Boundary response schemas (pydantic)."""

from __future__ import annotations

from pydantic import BaseModel, Field


class FailureResult(BaseModel):
    """Structured failure returned when input validation or solve fails."""

    code: str = Field(..., min_length=1)
    message: str = Field(..., min_length=1)


class FailureResponse(BaseModel):
    """Structured failure envelope for invalid boundary input."""

    type: str = Field(default="ERROR")
    code: str = Field(..., min_length=1)
    message: str = Field(..., min_length=1)


class ValidationSuccess(BaseModel):
    """Pass signal when FR-01 input validation succeeds."""

    type: str = Field(default="OK")


class SuccessResponse(BaseModel):
    """Structured success envelope with int[6] solution data."""

    type: str = Field(default="OK")
    data: list[int] = Field(..., min_length=6, max_length=6)
