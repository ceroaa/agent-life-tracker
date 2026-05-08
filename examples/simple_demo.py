from agent_life_tracker import AgentLifeTracker


def main() -> None:
    tracker = AgentLifeTracker(state_path=".demo_state/simple.json")
    tracker.start_focus("DEMO-001", "Prepare release notes", source="mainline")
    tracker.update_step(
        "DEMO-001",
        step="Drafted release note outline.",
        status="drafted",
        next_hint="Review the changelog before publishing.",
    )
    tracker.mark_done("DEMO-001", "Release notes were drafted and reviewed.")
    print(tracker.status()["archive_summary"])


if __name__ == "__main__":
    main()

