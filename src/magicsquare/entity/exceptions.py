"""Domain-level exceptions for entity validation failures."""


class DomainError(Exception):
    """Base class for domain errors without UI message coupling."""


class InvalidUserError(DomainError):
    """Raised when User identity or display name violates invariants."""
