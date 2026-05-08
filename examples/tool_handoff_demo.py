from agent_life_tracker import AgentLifeTracker


def main() -> None:
    tracker = AgentLifeTracker(state_path=".demo_state/handoff.json")
    tracker.start_focus("DEMO-002", "Investigate stuck import job", source="operator")
    tracker.record_note(
        "DEMO-002",
        role="tool_a",
        status="diagnosed",
        summary="The import job reached validation but did not start writing output.",
        next_hint="Check the output writer initialization path.",
    )
    tracker.record_handoff(
        "DEMO-002",
        from_role="tool_a",
        to_role="tool_b",
        reason="Diagnosis complete; implementation tool should continue.",
        summary="Validation completed before the output writer started.",
        next_hint="Inspect output writer initialization.",
    )
    print(tracker.format_handoff_context("DEMO-002"))


if __name__ == "__main__":
    main()

