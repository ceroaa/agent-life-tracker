# Agent Life Tracker

## Secretary Shadow Thread for Long-Running Agents

Agent Life Tracker is a small Python sidecar for agents that need to remember unfinished work without giving the attention system control over execution.

It is not an agent framework. It is not a scheduler. It is not an executor. It is not a memory database.

It is a sidecar continuity layer.

Tasks may pause.  
Tools may fail.  
Context may reset.  
But unfinished intentions should not die.

&#x4EFB;&#x52D9;&#x53EF;&#x4EE5;&#x66AB;&#x505C;&#x3002;

&#x5DE5;&#x5177;&#x53EF;&#x4EE5;&#x5931;&#x6557;&#x3002;

&#x4E0A;&#x4E0B;&#x6587;&#x53EF;&#x4EE5;&#x91CD;&#x7F6E;&#x3002;

&#x4F46;&#x672A;&#x5B8C;&#x6210;&#x7684;&#x610F;&#x5716;&#x4E0D;&#x8A72;&#x6B7B;&#x4EA1;&#x3002;

## Why

Most agent systems focus on execution. But long-running agents also need non-executive continuity.

A task may be blocked, waiting for approval, waiting for another tool, or paused after a timeout. If the system forgets it, the agent becomes short-lived. If the attention system takes control, it becomes noisy and resource-hungry.

Agent Life Tracker gives the system a secretary: not a controller, not an executor, only a keeper of unfinished intentions.

## Core Principle

Attention detects.  
Secretary remembers.  
Mainline decides.  
Tools execute.

&#x6CE8;&#x610F;&#x529B;&#x8CA0;&#x8CAC;&#x767C;&#x73FE;&#x3002;

&#x79D8;&#x66F8;&#x8CA0;&#x8CAC;&#x8A18;&#x4F4F;&#x3002;

&#x4E3B;&#x7DDA;&#x8CA0;&#x8CAC;&#x6C7A;&#x7B56;&#x3002;

&#x5DE5;&#x5177;&#x8CA0;&#x8CAC;&#x57F7;&#x884C;&#x3002;

## What It Tracks

- current focus
- pending attentions
- handoffs between tools
- archived outcomes

## What It Does Not Do

- It does not execute tasks.
- It does not schedule resources.
- It does not call tools.
- It does not modify priority queues.
- It does not replace your agent framework.
- It does not bypass human approval.
- It does not bypass your safety layer.
- It does not become the main controller.

Agent Life Tracker only:

- remembers unfinished intentions
- tracks stalled work
- records handoffs
- stores reminder cards
- exposes compact status to humans, agents, or tools

## Installation

```bash
pip install agent-life-tracker
```

From source:

```bash
git clone https://github.com/your-org/agent-life-tracker.git
cd agent-life-tracker
pip install -e .
```

## Quick Start

```python
from agent_life_tracker import AgentLifeTracker

tracker = AgentLifeTracker()

tracker.start_focus(
    focus_id="SX-001",
    title="Fix timeout in long-running agent",
    source="mainline",
)

tracker.record_note(
    focus_id="SX-001",
    role="diagnosis_tool",
    status="diagnosed",
    summary="The task appears to be queued but not executed.",
    next_hint="Inspect the queue consumer loop.",
)

tracker.record_handoff(
    focus_id="SX-001",
    from_role="diagnosis_tool",
    to_role="repair_tool",
    reason="Diagnosis complete; repair tool should continue.",
    next_hint="Check queue consumer loop.",
)

tracker.add_attention(
    focus_id="SX-001",
    severity="P2",
    message="Task has been queued for more than 3 hours.",
)

print(tracker.format_handoff_context("SX-001"))
```

Example output:

```text
[Agent Life Tracker]
focus_id: SX-001
title: Fix timeout in long-running agent
last_status: diagnosed
last_step: The task appears to be queued but not executed.
next_hint: Inspect the queue consumer loop.
pending: P2 - Task has been queued for more than 3 hours.
handoff: diagnosis_tool -> repair_tool
```

## Storage

The default state path is:

```text
.agent_life_tracker/state.json
```

You can pass a custom path:

```python
tracker = AgentLifeTracker(state_path="runtime/agent_state.json")
```

JSON writes use a temporary file, flush, fsync, and atomic replace. A small lock file helps avoid half-written state during concurrent writes.

## Use Cases

- long-running coding agents
- multi-tool agent handoffs
- timeout recovery
- human-in-the-loop workflows
- persistent task tracking
- sidecar memory for unfinished work
- agent operation logs

## Philosophy

The secretary is not the brain.  
The secretary is not the hand.  
The secretary is the notebook that stays open when everything else changes.

&#x79D8;&#x66F8;&#x4E0D;&#x662F;&#x5927;&#x8166;&#x3002;

&#x79D8;&#x66F8;&#x4E0D;&#x662F;&#x624B;&#x3002;

&#x79D8;&#x66F8;&#x662F;&#x6240;&#x6709;&#x6771;&#x897F;&#x90FD;&#x8B8A;&#x4E86;&#x4EE5;&#x5F8C;&#xFF0C;&#x4ECD;&#x7136;&#x6504;&#x958B;&#x5728;&#x684C;&#x4E0A;&#x7684;&#x90A3;&#x672C;&#x7B46;&#x8A18;&#x3002;

## Origin

This project was inspired by experiments in Xiaoyu City, but it does not include Xiaoyu City's private runtime, memory, identity layer, prompts, API keys, task logs, or internal control system.

It only publishes a general-purpose sidecar pattern for tracking unfinished work in long-running agents.

&#x672C;&#x5DE5;&#x5177;&#x62BD;&#x8C61;&#x81EA;&#x5C0F;&#x96E8;&#x57CE;&#x9577;&#x671F; Agent &#x5BE6;&#x9A57;&#x4E2D;&#x7684;&#x4E00;&#x500B;&#x901A;&#x7528;&#x6A21;&#x5F0F;&#xFF0C;&#x4F46;&#x4E0D;&#x5305;&#x542B;&#x5C0F;&#x96E8;&#x57CE;&#x672C;&#x9AD4;&#x3001;&#x4E0D;&#x5305;&#x542B;&#x79C1;&#x6709;&#x8A18;&#x61B6;&#x3001;&#x4E0D;&#x5305;&#x542B;&#x8EAB;&#x4EFD;&#x5C64;&#x3001;&#x4E0D;&#x5305;&#x542B; prompt&#x3001;&#x4E0D;&#x5305;&#x542B; API key&#x3001;&#x4E0D;&#x5305;&#x542B;&#x4EFB;&#x52D9;&#x7D00;&#x9304;&#x3001;&#x4E0D;&#x5305;&#x542B;&#x5167;&#x90E8;&#x63A7;&#x5236;&#x93C8;&#x3002;

&#x9019;&#x91CC;&#x53EA;&#x958B;&#x6E90;&#x4E00;&#x500B;&#x901A;&#x7528;&#x5C0F;&#x5DE5;&#x5177;&#xFF1A;&#x7528;&#x4F86;&#x8FFD;&#x8E64;&#x9577;&#x671F; Agent &#x7684;&#x672A;&#x5B8C;&#x6210;&#x4EFB;&#x52D9;&#x3001;&#x63D0;&#x9192;&#x8207;&#x5DE5;&#x5177;&#x4EA4;&#x63A5;&#x3002;
