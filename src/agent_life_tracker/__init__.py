"""Agent Life Tracker: a sidecar continuity layer for long-running agents."""

from .exceptions import (
    AgentLifeTrackerError,
    FocusNotFoundError,
    InvalidSeverityError,
    StateLockTimeoutError,
)
from .tracker import AgentLifeTracker

__all__ = [
    "AgentLifeTracker",
    "AgentLifeTrackerError",
    "FocusNotFoundError",
    "InvalidSeverityError",
    "StateLockTimeoutError",
]

__version__ = "0.1.0"
