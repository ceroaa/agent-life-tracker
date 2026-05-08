import json

from agent_life_tracker import AgentLifeTracker


def test_atomic_write_leaves_valid_json(tmp_path):
    state_path = tmp_path / "state.json"
    tracker = AgentLifeTracker(state_path)
    tracker.start_focus("F-1", "Atomic write")
    tracker.update_step("F-1", "Write completed.", "updated")
    with state_path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    assert data["current"]["focus_id"] == "F-1"


def test_repeated_pending_attention_deduplicates_and_counts(tmp_path):
    tracker = AgentLifeTracker(tmp_path / "state.json")
    tracker.start_focus("F-1", "Avoid state growth")
    for _ in range(20):
        tracker.add_attention("F-1", "P2", "The same pending work remains.")
    attentions = tracker.status()["pending_attentions"]
    assert len(attentions) == 1
    assert attentions[0]["remind_count"] == 20
    assert attentions[0]["still_active"] is True


def test_many_distinct_attentions_are_capped(tmp_path):
    tracker = AgentLifeTracker(tmp_path / "state.json")
    tracker.start_focus("F-1", "Avoid state explosion")
    for index in range(130):
        tracker.add_attention("F-1", "P3", f"Pending item {index}")
    assert len(tracker.status()["pending_attentions"]) == 100

