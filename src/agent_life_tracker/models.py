"""Typed state models for Agent Life Tracker."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional


VERSION = "0.1.0"
SEVERITIES = {"P0", "P1", "P2", "P3"}


@dataclass
class CurrentFocus:
    """The active focus currently being kept alive by the sidecar."""

    focus_id: str
    title: str
    owner: str
    status: str
    last_step: str
    next_hint: str
    created_at: str
    updated_at: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Attention:
    """A reminder card for unfinished or stalled work."""

    id: str
    focus_id: str
    severity: str
    message: str
    source: str
    remind_count: int
    still_active: bool
    created_at: str
    updated_at: str


@dataclass
class Handoff:
    """A compact record of one tool or role handing work to another."""

    id: str
    focus_id: str
    from_role: str
    to_role: str
    reason: str
    summary: str
    next_hint: str
    created_at: str


@dataclass
class ArchiveEntry:
    """A closed focus, retained as a short outcome record."""

    focus_id: str
    title: str
    final_status: str
    result_summary: str
    closed_at: str


@dataclass
class TrackerState:
    """The complete JSON state shape stored by Agent Life Tracker."""

    version: str = VERSION
    current: Optional[CurrentFocus] = None
    pending_attentions: List[Attention] = field(default_factory=list)
    handoffs: List[Handoff] = field(default_factory=list)
    archive: List[ArchiveEntry] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Return a JSON-serializable dictionary."""

        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TrackerState":
        """Build a typed state object from stored JSON data."""

        current_data = data.get("current")
        return cls(
            version=str(data.get("version") or VERSION),
            current=CurrentFocus(**current_data) if current_data else None,
            pending_attentions=[
                Attention(**item) for item in data.get("pending_attentions", [])
            ],
            handoffs=[Handoff(**item) for item in data.get("handoffs", [])],
            archive=[ArchiveEntry(**item) for item in data.get("archive", [])],
        )

