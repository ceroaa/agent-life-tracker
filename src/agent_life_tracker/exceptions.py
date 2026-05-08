"""Exceptions raised by Agent Life Tracker."""


class AgentLifeTrackerError(Exception):
    """Base exception for all tracker errors."""


class FocusNotFoundError(AgentLifeTrackerError):
    """Raised when a requested focus does not exist in current state."""


class InvalidSeverityError(AgentLifeTrackerError):
    """Raised when an attention severity is not one of P0, P1, P2, or P3."""


class StateLockTimeoutError(AgentLifeTrackerError):
    """Raised when the state file lock cannot be acquired in time."""

