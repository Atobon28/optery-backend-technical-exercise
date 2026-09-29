# Interviewer Guide — INTERNAL ONLY

Do not share this file with candidates.

## What this exercise measures

Mandatory dimensions:
1. Python Backend Engineering & System Design
2. Databases & Data Integrity
3. Distributed Systems & Reliability
4. Production Debugging & Performance

Entry criterion: candidate starts an unfamiliar project in under 3 minutes.

Django is a preference, not a requirement.

## Part 0 — Start project

Ask: Please get this project running locally. Talk us through what you're doing as you go.

Pass: running in under 3 minutes without step-by-step guidance.

## Part 1 — Backend Engineering & System Design

Ask the candidate to explain the workflow, identify the most important production risk, implement a fix, and explain an alternative they considered.

Expected signal: concrete reasoning, working code, and a clear trade-off.

## Part 2 — Databases & Data Integrity

Intentional issue: two workers may read the same non-completed row and both proceed.

Ask what can go wrong if two workers process the same record almost simultaneously, then ask the candidate to make it safe and explain how they would verify correctness.

Strong answers may include an atomic state transition, row-level locking on a production database, or another database-backed ownership mechanism.

## Part 3 — Distributed Systems & Reliability

Intentional issue: the external provider side effect can succeed before our application records success. A retry may repeat the external action.

Ask what happens if the worker crashes after the provider succeeds but before success is stored, then ask how to make retries safe. Follow with an ambiguous-timeout scenario.

Strong answers may include persisted idempotency keys, provider-side idempotency, explicit operation state, reconciliation, or another concrete mechanism that avoids duplicate business outcomes.

## Part 4 — Production Debugging & Performance

Intentional issue: the list endpoint performs a repeated COUNT query inside a loop.

Tell the candidate the endpoint moved from roughly 200 ms to around 2 seconds and ask how they would investigate, identify root cause, implement a fix, and prove improvement.

Strong evidence includes hypotheses, query inspection, measurable before/after data, and a fix that reduces repeated database work.

## Standardized hints

Hint 0: no help.
Hint 1: direction only.
Hint 2: point to the system area.
Hint 3: name the concept.

Examples:
- Hint 1: Take another look at what happens if this operation executes twice.
- Hint 2: Look at how state is handled between the database and the external operation.
- Hint 3: Think about idempotency and what needs to persist across retries.

Record every hint and what happened immediately after it.

## Evidence block per candidate

Record:
- What they solved independently
- What they solved after hints
- Highest hint level used
- What they could not solve
- What was not tested
- Observable evidence per mandatory dimension
- Optional Django, cloud, and backend ecosystem signals

Never treat “not tested” as positive or negative evidence.
