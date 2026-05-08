from agent_life_tracker import AgentLifeTracker


def test_add_attention_records_active_card(tmp_path):
    tracker = AgentLifeTracker(tmp_path / "state.json")
    tracker.start_focus("F-1", "Track reminder")
    tracker.add_attention("F-1", "P2", "Task has been queued too long.", "watcher")
    attention = tracker.status()["pending_attentions"][0]
    assert attention["severity"] == "P2"
    assert attention["remind_count"] == 1
    assert attention["still_active"] is True


def test_record_handoff_saves_roles_and_reason(tmp_path):
    tracker = AgentLifeTracker(tmp_path / "state.json")
    tracker.start_focus("F-1", "Repair stalled job")
    tracker.record_handoff(
        "F-1",
        from_role="tool_a",
        to_role="tool_b",
        reason="Diagnosis complete.",
        next_hint="Continue at output writer.",
    )
    handoff = tracker.status()["handoffs"][0]
    assert handoff["from_role"] == "tool_a"
    assert handoff["to_role"] == "tool_b"
    assert handoff["reason"] == "Diagnosis complete."


def test_handoff_context_mentions_latest_handoff(tmp_path):
    tracker = AgentLifeTracker(tmp_path / "state.json")
    tracker.start_focus("F-1", "Repair stalled job")
    tracker.record_note(
        "F-1",
        role="tool_a",
        status="diagnosed",
        summary="The writer did not start.",
        next_hint="Inspect writer setup.",
    )
    tracker.record_handoff("F-1", "tool_a", "tool_b", "Continue repair.")
    text = tracker.format_handoff_context("F-1")
    assert "handoff: tool_a -> tool_b" in text
    assert "last_status: diagnosed" in text
