# Secretary Shadow Thread:
# A Hidden Continuity Layer for Long-Running Agents

## 1. Problem: short-lived agents forget unfinished work

Many agents can call tools, write code, run checks, and produce output. The harder problem appears after interruption.

A tool times out. A model call falls back. A human approval is needed. A coding agent hands work to a verifier. A session ends before the final step. Without a continuity layer, the next actor may know the latest visible message but not the unfinished intention.

The result is not just lost context. It is lost responsibility.

## 2. Bad solution: attention system takes over resources

One tempting fix is to let the attention system become active. It detects stalled work, then schedules retries, changes priorities, calls tools, and competes with the mainline.

That usually creates a noisier system. Attention becomes an owner of resources. Reminder logic becomes execution logic. The mechanism that should notice unfinished work starts deciding what should happen next.

## 3. Pattern: secretary as sidecar continuity layer

The Secretary Shadow Thread is a sidecar pattern:

- attention detects
- secretary remembers
- mainline decides
- tools execute

The secretary is deliberately passive. It stores the current focus, reminders, handoffs, and outcomes. It exposes concise context to the next human, agent, or tool.

It does not own the system.

## 4. State model: current / pending_attentions / handoffs / archive

The state model has four parts:

- `current`: the active focus, title, status, last step, next hint, timestamps, and caller-owned metadata
- `pending_attentions`: reminder cards that describe stalled or unfinished work
- `handoffs`: short records of one role or tool passing work to another
- `archive`: done or abandoned outcomes

The state file is intentionally small JSON. It is easy to inspect, back up, diff, and repair.

## 5. Rule: secretary remembers, but never executes

Agent Life Tracker must not:

- execute tasks
- schedule resources
- call external tools
- modify priority queues
- bypass human approval
- bypass safety gates
- become the main controller

Agent Life Tracker only:

- remembers unfinished intentions
- tracks stalled work
- records handoffs
- stores reminder cards
- exposes compact status to humans, agents, or tools

## 6. Integration examples

A coding agent can call `record_note()` before running a long check, then call `update_step()` after the check finishes.

A timeout guard can call `add_attention()` when a tool stops before its verification step.

A diagnosis tool can call `record_handoff()` when it has enough information for a repair tool to continue.

A user interface can call `status()` to show the current focus and pending reminders.

An LLM prompt builder can call `format_handoff_context()` to pass compact state into the next session without exposing full metadata.

## 7. Limitations

This pattern is not a durable workflow engine. It does not enforce exactly-once execution. It does not resolve conflicts between multiple active controllers. It does not replace an audit log, database, message queue, scheduler, or agent framework.

It is a small continuity layer. Its job is to keep unfinished intentions visible.

## 8. Safety boundaries

This project was inspired by experiments in Xiaoyu City, but it does not include Xiaoyu City's private runtime, memory, identity layer, prompts, API keys, task logs, or internal control system.

It only publishes a general-purpose sidecar pattern for tracking unfinished work in long-running agents.

