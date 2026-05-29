"""User entity — puzzle player identity for save/load ownership (DATA layer id)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar

from magicsquare.entity.exceptions import InvalidUserError


@dataclass(frozen=True, slots=True)
class User:
    """Immutable puzzle player identity.

    Associates saved puzzles (Repository ``id``) with a stable owner. Holds no
    I/O, authentication, or boundary concerns.

    Attributes:
        user_id: Unique non-empty identifier after normalization.
        display_name: Human-readable label, 1..MAX_DISPLAY_NAME_LENGTH chars.
    """

    MAX_DISPLAY_NAME_LENGTH: ClassVar[int] = 50

    user_id: str
    display_name: str

    @classmethod
    def create(cls, user_id: str, display_name: str) -> User:
        """Build a validated ``User`` from raw strings.

        Args:
            user_id: External id; leading/trailing whitespace is stripped.
            display_name: Label shown in UI; stripped and length-checked.

        Returns:
            A frozen ``User`` instance.

        Raises:
            InvalidUserError: If ``user_id`` or ``display_name`` is invalid.
        """
        normalized_id = cls._normalize(user_id)
        normalized_name = cls._normalize(display_name)
        cls._validate_user_id(normalized_id)
        cls._validate_display_name(normalized_name)
        return cls(user_id=normalized_id, display_name=normalized_name)

    def __eq__(self, other: object) -> bool:
        """Compare users by ``user_id`` only."""
        if not isinstance(other, User):
            return NotImplemented
        return self.user_id == other.user_id

    def __hash__(self) -> int:
        """Hash by ``user_id`` for use in sets and dict keys."""
        return hash(self.user_id)

    @staticmethod
    def _normalize(value: str) -> str:
        """Strip leading and trailing whitespace."""
        return value.strip()

    @classmethod
    def _validate_user_id(cls, user_id: str) -> None:
        """Ensure ``user_id`` is non-empty after normalization."""
        if not user_id:
            raise InvalidUserError("user_id must not be empty")

    @classmethod
    def _validate_display_name(cls, display_name: str) -> None:
        """Ensure ``display_name`` length is within allowed bounds."""
        if not display_name:
            raise InvalidUserError("display_name must not be empty")
        if len(display_name) > cls.MAX_DISPLAY_NAME_LENGTH:
            raise InvalidUserError(
                "display_name must be at most "
                f"{cls.MAX_DISPLAY_NAME_LENGTH} characters"
            )
