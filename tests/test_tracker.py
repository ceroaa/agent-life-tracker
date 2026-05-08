import json

from agent_life_tracker import AgentLifeTracker


def test_initializes_state_file(tmp_path):
    state_path = tmp_path / "state.json"
    AgentLifeTracker(state_path=state_path)
    assert state_path.exists()
    assert json.loads(state_path.read_text(encoding="utf-8"))["version"] == "0.1.0"


def test_start_focus_creates_current(tmp_path):
    tracker = AgentLifeTracker(tmp_path / "state.json")
    tracker.start_focus("F-1", "Fix timeout", source="mainline")
    current = tracker.status()["current"]
    assert current["focus_id"] == "F-1"
    assert current["title"] == "Fix timeout"
    assert current["owner"] == "mainline"


def test_update_step_updates_status_last_step_and_next_hint(tmp_path):
    tracker = AgentLifeTracker(tmp_path / "state.json")
    tracker.start_focus("F-1", "Fix timeout")
    tracker.update_step(
        "F-1",
        step="Checked worker state.",
        status="diagnosed",
        next_hint="Inspect retry handling.",
    )
    current = tracker.status()["current"]
    assert current["status"] == "diagnosed"
    assert current["last_step"] == "Checked worker state."
    assert current["next_hint"] == "Inspect retry handling."


def test_mark_done_moves_current_to_archive(tmp_path):
    tracker = AgentLifeTracker(tmp_path / "state.json")
    tracker.start_focus("F-1", "Finish report")
    tracker.mark_done("F-1", "Report completed.")
    status = tracker.status()
    assert status["current"] is None
    assert status["archive"][0]["focus_id"] == "F-1"
    assert status["archive"][0]["final_status"] == "done"


def test_format_handoff_context_omits_metadata(tmp_path):
    tracker = AgentLifeTracker(tmp_path / "state.json")
    tracker.start_focus(
        "F-1",
        "Fix timeout",
        metadata={"private_note": "do-not-print", "redacted_value": "hidden"},
    )
    tracker.update_step("F-1", "Queued for repair.", "queued")
    text = tracker.format_handoff_context("F-1")
    assert "do-not-print" not in text
    assert "metadata" not in text
    assert "focus_id: F-1" in text


def test_summary_is_truncated(tmp_path):
    tracker = AgentLifeTracker(tmp_path / "state.json")
    tracker.start_focus("F-1", "Long summary")
    tracker.update_step("F-1", "x" * 1000, "running")
    last_step = tracker.status()["current"]["last_step"]
    assert len(last_step) <= 500
    assert last_step.endswith("[truncated]")



