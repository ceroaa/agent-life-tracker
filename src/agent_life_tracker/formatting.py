"""Human and agent-facing formatting helpers."""

from __future__ import annotations

from typing import Optional

from .models import TrackerState


def format_handoff_context(state: TrackerState, focus_id: Optional[str] = None) -> str:
    """Return a compact prompt-safe handoff summary.

    Metadata is intentionally omitted because callers may store private routing
    details, local paths, or user-specific data there.
    """

    current = state.current
    if not current:
        return "[Agent Life Tracker]\ncurrent: none"
    if focus_id and current.focus_id != focus_id:
        return f"[Agent Life Tracker]\nfocus_id: {focus_id}\ncurrent: not found"

    attentions = [
        item for item in state.pending_attentions if item.focus_id == current.focus_id
    ]
    handoffs = [item for item in state.handoffs if item.focus_id == current.focus_id]

    lines = [
        "[Agent Life Tracker]",
        f"focus_id: {current.focus_id}",
        f"title: {current.title}",
        f"last_status: {current.status}",
        f"last_step: {current.last_step}",
        f"next_hint: {current.next_hint}",
    ]
    for attention in attentions[:3]:
        lines.append(f"pending: {attention.severity} - {attention.message}")
    if len(attentions) > 3:
        lines.append(f"pending_more: {len(attentions) - 3}")
    if handoffs:
        last_handoff = handoffs[-1]
        lines.append(f"handoff: {last_handoff.from_role} -> {last_handoff.to_role}")
        if last_handoff.next_hint:
            lines.append(f"handoff_next: {last_handoff.next_hint}")
    return "\n".join(lines)

