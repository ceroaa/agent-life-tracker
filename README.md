# Agent Life Tracker

## Secretary Shadow Thread for Long-Running Agents

Agent Life Tracker is a small Python sidecar for agents that need to remember unfinished work without giving the attention system control over execution.

It is not an agent framework. It is not a scheduler. It is not an executor. It is not a memory database.

It is a sidecar continuity layer.

Tasks may pause.  
Tools may fail.  
Context may reset.  
But unfinished intentions should not die.

隞餃??臭誑?怠??? 
撌亙?臭誑憭望??? 
銝??隞仿?蝵柴? 
雿摰?????閰脫香鈭～?
## Why

Most agent systems focus on execution. But long-running agents also need non-executive continuity.

A task may be blocked, waiting for approval, waiting for another tool, or paused after a timeout. If the system forgets it, the agent becomes short-lived. If the attention system takes control, it becomes noisy and resource-hungry.

Agent Life Tracker gives the system a secretary: not a controller, not an executor, only a keeper of unfinished intentions.

Agent Life Tracker ?臭??策?瑟? Agent ?函??餈質馱?具?
摰?霈?Agent 霈??游?? 
摰?霈釣??蝟餌絞???? 
摰?霈??霈?隤踹漲?具?
摰??隞嗡?嚗??芸?????????
隞餃??臭誑?怠??極?瑕隞?timeout??銝??臭誑?????芸???銝餌?銝?閰脫?憭晞?
## Core Principle

Attention detects.  
Secretary remembers.  
Mainline decides.  
Tools execute.

瘜冽???鞎祉?整? 
蝘鞎痊閮??? 
銝餌?鞎痊瘙箇??? 
撌亙鞎痊?瑁???
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

蝘銝憭扯?? 
蝘銝?? 
蝘?舀??镼輸霈?隞亙?嚗??嗆?獢???祉?閮?
## Origin

This project was inspired by experiments in Xiaoyu City, but it does not include Xiaoyu City's private runtime, memory, identity layer, prompts, API keys, task logs, or internal control system.

It only publishes a general-purpose sidecar pattern for tracking unfinished work in long-running agents.

?砍極?瑟鞊∟撠???Agent 撖阡?銝剔?銝?璅∪?嚗?銝??怠??典??祇????蝘?閮???頨思遢撅扎?? prompt??? API key???隞餃?蝝????折?批??
餈??芷?皞??撠極?瘀??其?餈質馱?瑟? Agent ?摰?隞餃?????撌亙鈭斗??

