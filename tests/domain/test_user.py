"""Domain tests for User entity (DOM-USER-*)."""

from __future__ import annotations

import pytest

from magicsquare.entity.exceptions import InvalidUserError
from magicsquare.entity.user import User


class TestUserCreate:
    """User.create factory validation."""

    def test_user_create_valid_ids_returns_user(self) -> None:
        # Arrange
        user_id = "player-001"
        display_name = "Magic Player"

        # Act
        user = User.create(user_id=user_id, display_name=display_name)

        # Assert
        assert user.user_id == "player-001"
        assert user.display_name == "Magic Player"

    def test_user_create_strips_whitespace_returns_normalized_user(self) -> None:
        # Arrange
        user_id = "  player-002  "
        display_name = "  Solver  "

        # Act
        user = User.create(user_id=user_id, display_name=display_name)

        # Assert
        assert user.user_id == "player-002"
        assert user.display_name == "Solver"

    def test_user_create_empty_user_id_raises_invalid_user_error(self) -> None:
        # Arrange
        user_id = ""
        display_name = "Player"

        # Act / Assert
        with pytest.raises(InvalidUserError, match="user_id"):
            User.create(user_id=user_id, display_name=display_name)

    def test_user_create_whitespace_only_user_id_raises_invalid_user_error(
        self,
    ) -> None:
        # Arrange
        user_id = "   "
        display_name = "Player"

        # Act / Assert
        with pytest.raises(InvalidUserError, match="user_id"):
            User.create(user_id=user_id, display_name=display_name)

    def test_user_create_empty_display_name_raises_invalid_user_error(self) -> None:
        # Arrange
        user_id = "player-003"
        display_name = ""

        # Act / Assert
        with pytest.raises(InvalidUserError, match="display_name"):
            User.create(user_id=user_id, display_name=display_name)

    def test_user_create_display_name_too_long_raises_invalid_user_error(
        self,
    ) -> None:
        # Arrange
        user_id = "player-004"
        display_name = "x" * (User.MAX_DISPLAY_NAME_LENGTH + 1)

        # Act / Assert
        with pytest.raises(InvalidUserError, match="display_name"):
            User.create(user_id=user_id, display_name=display_name)


class TestUserEquality:
    """Identity equality by user_id."""

    def test_user_equality_same_user_id_returns_true(self) -> None:
        # Arrange
        first = User.create(user_id="same-id", display_name="Alice")
        second = User.create(user_id="same-id", display_name="Bob")

        # Act / Assert
        assert first == second

    def test_user_inequality_different_user_id_returns_false(self) -> None:
        # Arrange
        first = User.create(user_id="id-a", display_name="Alice")
        second = User.create(user_id="id-b", display_name="Alice")

        # Act / Assert
        assert first != second

    def test_user_hash_same_user_id_equal_hashes(self) -> None:
        # Arrange
        first = User.create(user_id="hash-id", display_name="One")
        second = User.create(user_id="hash-id", display_name="Two")

        # Act / Assert
        assert hash(first) == hash(second)
