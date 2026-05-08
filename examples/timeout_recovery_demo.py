from agent_life_tracker import AgentLifeTracker


def main() -> None:
    tracker = AgentLifeTracker(state_path=".demo_state/timeout.json")
    tracker.start_focus("DEMO-003", "Recover after long tool timeout", source="mainline")
    tracker.update_step(
        "DEMO-003",
        step="Tool timed out while checking generated artifacts.",
        status="timeout",
        next_hint="Resume by listing generated artifacts and verifying checksums.",
    )
    tracker.add_attention(
        "DEMO-003",
        severity="P1",
        message="Verification stopped after timeout and still needs continuation.",
        source="timeout_guard",
    )
    print(tracker.format_handoff_context("DEMO-003"))


if __name__ == "__main__":
    main()

