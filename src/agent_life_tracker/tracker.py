"""Public tracker API for the Secretary Shadow Thread pattern."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional
from uuid import uuid4

from .exceptions import FocusNotFoundError, InvalidSeverityError
from .formatting import format_handoff_context as render_handoff_context
from .models import (
    SEVERITIES,
    ArchiveEntry,
    Attention,
    CurrentFocus,
    Handoff,
    TrackerState,
)
from .storage import JsonStorage


MAX_TEXT_LENGTH = 500
MAX_TITLE_LENGTH = 180
MAX_PENDING_ATTENTIONS = 100
MAX_HANDOFFS = 100
MAX_ARCHIVE = 200


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _truncate(value: Optional[str], limit: int = MAX_TEXT_LENGTH) -> str:
    if not value:
        return ""
    text = " ".join(str(value).split())
    if len(text) <= limit:
        return text
    suffix = "...[truncated]"
    return text[: max(0, limit - len(suffix))].rstrip() + suffix


class AgentLifeTracker:
    """A tiny sidecar continuity layer for long-running agents.

    The tracker remembers unfinished intentions, stalled work, tool handoffs,
    and closed outcomes. It never executes work, schedules resources, calls
    external tools, or becomes the main controller.
    """

    def __init__(self, state_path: Optional[str | Path] = None) -> None:
        self.storage = JsonStorage(state_path)
        self.storage.initialize()

    def start_focus(
        self,
        focus_id: str,
        title: str,
        source: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Start tracking a mainline focus."""

        state = self._load()
        now = _now()
        state.current = CurrentFocus(
            focus_id=focus_id,
            title=_truncate(title, MAX_TITLE_LENGTH),
            owner=_truncate(source or ""),
            status="started",
            last_step="",
            next_hint="",
            created_at=now,
            updated_at=now,
            metadata=dict(metadata or {}),
        )
        self._save(state)
        return state.to_dict()

    def update_step(
        self,
        focus_id: str,
        step: str,
        status: str,
        summary: Optional[str] = None,
        next_hint: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Update the active focus with the latest progress."""

        state = self._load()
        current = self._require_current(state, focus_id)
        current.status = _truncate(status, 80)
        current.last_step = _truncate(summary or step)
        current.next_hint = _truncate(next_hint)
        current.updated_at = _now()
        self._save(state)
        return state.to_dict()

    def add_attention(
        self,
        focus_id: str,
        severity: str,
        message: str,
        source: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Add or refresh a pending attention card."""

        if severity not in SEVERITIES:
            raise InvalidSeverityError(f"Invalid severity: {severity}")
        state = self._load()
        self._require_current(state, focus_id)
        normalized_message = _truncate(message)
        now = _now()
        for attention in state.pending_attentions:
            if (
                attention.focus_id == focus_id
                and attention.severity == severity
                and attention.message == normalized_message
                and attention.still_active
            ):
                attention.remind_count += 1
                attention.updated_at = now
                if source:
                    attention.source = _truncate(source, 120)
                self._save(state)
                return state.to_dict()

        state.pending_attentions.append(
            Attention(
                id=uuid4().hex,
                focus_id=focus_id,
                severity=severity,
                message=normalized_message,
                source=_truncate(source or "", 120),
                remind_count=1,
                still_active=True,
                created_at=now,
                updated_at=now,
            )
        )
        state.pending_attentions = state.pending_attentions[-MAX_PENDING_ATTENTIONS:]
        self._save(state)
        return state.to_dict()

    def record_handoff(
        self,
        focus_id: str,
        from_role: str,
        to_role: str,
        reason: str,
        summary: Optional[str] = None,
        next_hint: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Record a handoff between roles, tools, or agent sessions."""

        state = self._load()
        current = self._require_current(state, focus_id)
        current.next_hint = _truncate(next_hint) or current.next_hint
        current.updated_at = _now()
        state.handoffs.append(
            Handoff(
                id=uuid4().hex,
                focus_id=focus_id,
                from_role=_truncate(from_role, 120),
                to_role=_truncate(to_role, 120),
                reason=_truncate(reason),
                summary=_truncate(summary),
                next_hint=_truncate(next_hint),
                created_at=_now(),
            )
        )
        state.handoffs = state.handoffs[-MAX_HANDOFFS:]
        self._save(state)
        return state.to_dict()

    def record_note(
        self,
        focus_id: str,
        role: str,
        status: str,
        summary: str,
        next_hint: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Record a short note left by a role or tool."""

        return self.update_step(
            focus_id=focus_id,
            step=f"{role}: {summary}",
            status=status,
            summary=summary,
            next_hint=next_hint,
        )

    def mark_done(self, focus_id: str, result_summary: str) -> Dict[str, Any]:
        """Close the focus as done and move it into the archive."""

        return self._close(focus_id, "done", result_summary)

    def mark_abandoned(self, focus_id: str, reason: str) -> Dict[str, Any]:
        """Close the focus as abandoned and move it into the archive."""

        return self._close(focus_id, "abandoned", reason)

    def status(self, focus_id: Optional[str] = None) -> Dict[str, Any]:
        """Return current state, optionally filtered to one focus."""

        state = self._load()
        data = state.to_dict()
        if not focus_id:
            data["archive_summary"] = self._archive_summary(state)
            return data
        data["pending_attentions"] = [
            item for item in data["pending_attentions"] if item["focus_id"] == focus_id
        ]
        data["handoffs"] = [
            item for item in data["handoffs"] if item["focus_id"] == focus_id
        ]
        data["archive"] = [item for item in data["archive"] if item["focus_id"] == focus_id]
        data["archive_summary"] = self._archive_summary(state)
        if data["current"] and data["current"]["focus_id"] != focus_id:
            data["current"] = None
        return data

    def format_handoff_context(self, focus_id: Optional[str] = None) -> str:
        """Return compact context suitable for an LLM or external tool prompt."""

        return render_handoff_context(self._load(), focus_id)

    def _close(self, focus_id: str, final_status: str, result_summary: str) -> Dict[str, Any]:
        state = self._load()
        current = self._require_current(state, focus_id)
        state.archive.append(
            ArchiveEntry(
                focus_id=current.focus_id,
                title=current.title,
                final_status=final_status,
                result_summary=_truncate(result_summary),
                closed_at=_now(),
            )
        )
        state.archive = state.archive[-MAX_ARCHIVE:]
        state.current = None
        for attention in state.pending_attentions:
            if attention.focus_id == focus_id:
                attention.still_active = False
                attention.updated_at = _now()
        self._save(state)
        return state.to_dict()

    def _load(self) -> TrackerState:
        return TrackerState.from_dict(self.storage.read())

    def _save(self, state: TrackerState) -> None:
        self.storage.write(state.to_dict())

    @staticmethod
    def _require_current(state: TrackerState, focus_id: str) -> CurrentFocus:
        if not state.current or state.current.focus_id != focus_id:
            raise FocusNotFoundError(f"Focus is not current: {focus_id}")
        return state.current

    @staticmethod
    def _archive_summary(state: TrackerState) -> Dict[str, int]:
        done = sum(1 for item in state.archive if item.final_status == "done")
        abandoned = sum(1 for item in state.archive if item.final_status == "abandoned")
        return {"total": len(state.archive), "done": done, "abandoned": abandoned}
