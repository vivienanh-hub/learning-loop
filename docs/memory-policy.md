# Memory Policy

Learning Loop uses four kinds of memory. The architecture describes where information lives; this policy decides whether information is allowed to persist and influence future behaviour.

## Architecture

| Memory type | Purpose | Typical store | Persistence rule |
|---|---|---|---|
| Working | Current conversation and task state | Context window | Ends with the task unless admitted elsewhere |
| Episodic | Dated evidence of what happened | Session logs, decisions, issue history | May persist as evidence; is not automatically a claim about the learner |
| Semantic | Facts, goals, confirmed preferences, and supported patterns | `.claude/memory/` | Must satisfy the admission rule for its claim type |
| Procedural | Rules governing tutor or workflow behaviour | `.claude/commands/`, system instructions | Requires a verified defect, explicit user decision, or approved system change |

Keep three objects distinct:

- **Evidence:** an observable event or explicit statement.
- **Inference:** the system's interpretation of evidence.
- **Intervention:** a change in guidance or workflow intended to help.

An inference links to evidence. An intervention links to the inference or defect that justified it. Disputing an inference does not require deleting the underlying episode.

## Admission rules

| Claim type | Admission rule | Default review |
|---|---|---|
| Explicit fact, goal, constraint, or preference | Save when stated or confirmed by the learner; include provenance and date | At its stated horizon, on contradiction, or within 90 days for changeable facts |
| Session event | Save as episodic evidence only | Follow the journal's normal lifecycle |
| Behavioural inference | Create a candidate after three **independent** episodes within the last 30 days; require learner confirmation before broad use | Review within 60 days; expire within 90 days unless reconfirmed |
| Workflow defect | One reproduced incident may justify a procedural correction when the failure and fix are inspectable | Review after the next material use |
| Intervention | Store separately and state the expected effect | Evaluate after each material use; review after three uses or 30 days |
| Sensitive psychological, health, identity, or similarly high-impact inference | Never promote automatically; store only when the learner explicitly confirms the exact claim and intended use | Review within 30 days; default to expiry |

Independent episodes must come from distinct events. Copies, summaries, or multiple agents referring to the same original event count once.

## Founding records

Some records exist before the system has observed anything: the goal cascade in `system/feedback-loop.md`, the learner profile in `.claude/memory/user_profile.md`, and the work history in `personal-professional-profile/career/experience.yaml`. Every tutor reads at least one of them before it speaks, so they are durable claims and this policy governs them like any other. [The setup guide](memory-setup.md) shows the shape each one takes.

They are admitted under the explicit-fact rule — the learner states them, so they persist immediately. What they may not do is skip the metadata. A founding record carries `claim_type: explicit`, `status: confirmed`, a creation date, and `sources: self-declared at setup`. Naming the provenance that way is the point: it keeps a fact the learner asserted about themselves distinguishable from one the system worked out later, which is the distinction the rest of this policy is built on. Do not cite a source the system has no mechanism to produce.

Founding records describe changeable facts, so they review within 90 days like any other. A goal cascade nobody has revisited is not evidence of a stable goal; it is an unreviewed record, and `/goal-review` should treat it as one.

Genesis admits only what the learner declares about themselves at setup. It is not a route for the system's first impressions of them, and a record created any other way does not become founding by being early.

## Lifecycle

`Observe -> propose -> verify -> apply -> evaluate -> revalidate, retire, or delete`

- **Candidate:** inspectable but not allowed to shape general guidance.
- **Confirmed:** explicitly confirmed or admitted under a fact/defect rule.
- **Disputed:** contested by the learner; do not use while unresolved.
- **Retired:** historically useful but inactive.
- **Deleted:** remove the durable claim and derived uses. Keep source episodes only if the learner has not requested their deletion.

Contradictory evidence reopens a confirmed memory for review. Expired, disputed, and retired memories do not influence guidance unless the task is explicitly reviewing history.

## Required metadata

Use [the memory-record template](../examples/memory-record-template.md) for new records and for existing records when they are next materially edited. Do not invent missing dates or sources. Migrate legacy records as they are touched rather than rewriting the entire memory store at once.

At minimum, each durable record identifies:

- claim and memory type;
- candidate/confirmed/disputed/retired status;
- sensitivity;
- source evidence;
- creation, confirmation, review, and expiry dates;
- which tutors or workflows consume it;
- what behaviour it changes and how it can be falsified.

## Learner control

A context audit must let the learner:

- see each belief and why the system holds it;
- distinguish their own words from model inference;
- inspect evidence and downstream consumers;
- confirm, dispute, correct, retire, or delete a memory;
- see overdue reviews and observed effects.

Deletion removes the durable claim, its index entry, and any procedural rule derived only from it. Correction leaves an audit trail but must not leave the old wording active elsewhere.

## Effect evaluation

When a durable memory materially changes guidance or workflow behaviour, append an outcome to `journal/memory-effects.md`:

| Date | Memory | Consumer | Decision or intervention | Result | Evidence / follow-up |
|---|---|---|---|---|---|

Use one result: `helpful`, `irrelevant`, `stale`, or `harmful`.

Measure the learner outcome, not successful recall. A learning intervention is helpful when application or retrieval improves—not merely when the tutor repeats a pattern label.

## Safety boundaries

- Never turn one difficult week into a permanent trait.
- Never present model inference as the learner's own words.
- Do not retain sensitive information unrelated to learning.
- Prefer the least sensitive claim that supports the intended behaviour.
- Do not let an unconfirmed candidate change another tutor's behaviour.
- Public examples must be synthetic or deliberately redacted. Keep private memories and raw session excerpts out of public repositories.
