# Memory Setup

Learning Loop builds a persistent memory of who you are over time. This file explains the memory system and what you need to set up.

---

## How memory works

Claude Code has no persistent memory between conversations by default. Learning Loop solves this with a file-based memory system: structured Markdown files in `.claude/memory/` that are read at the start of relevant sessions.

The skills automatically read these files — you don't need to reference them explicitly.

The system separates four memory types: working memory in the current context, episodic evidence in dated journals, semantic facts and confirmed patterns in `.claude/memory/`, and procedural rules in command files. See [Memory Policy](memory-policy.md) for what each type is allowed to retain and how the learner can correct it.

---

## Required files

### `.claude/memory/MEMORY.md`

The index. Every memory file must have a one-line entry here so future sessions know to load it.

```markdown
- [user_profile.md](user_profile.md) — who you are, how you work
- [job_situation.md](job_situation.md) — current job search status
```

### `.claude/memory/user_profile.md`

Who you are and how you learn. The Mentor reads this to calibrate its voice. The Lab reads this to frame explanations.

```markdown
---
name: user-profile
description: Who the user is, how they learn, what they value
metadata:
  type: user
  memory_type: semantic
  claim_type: explicit
  status: confirmed
  sensitivity: low
  created: YYYY-MM-DD
  last_confirmed: YYYY-MM-DD
  review_by: YYYY-MM-DD
  expires: null
  sources:
    - onboarding
  consumers:
    - mentor
    - lab
---

Background: [your professional background in 2-3 sentences]
Domain: [your area of expertise]
Learning style: [how you learn best — examples, analogies, depth, etc.]
Working style: [how you prefer to engage with Claude]
Goal: [what you're trying to achieve right now]
```

### `.claude/memory/job_situation.md` (if job-searching)

Current status. The Mentor uses this to calibrate urgency in every session.

```markdown
---
name: job-situation
description: Current job search status and urgency
metadata:
  type: project
  memory_type: semantic
  claim_type: explicit
  status: confirmed
  sensitivity: medium
  created: YYYY-MM-DD
  last_confirmed: YYYY-MM-DD
  review_by: YYYY-MM-DD
  expires: YYYY-MM-DD | null
  sources:
    - onboarding
  consumers:
    - mentor
    - cv-job-match
---

Status: [actively searching / open to opportunities / not looking]
Timeline: [any deadlines or urgency — e.g. "contract ends 2026-09"]
Target: [role type, company type, location]
Salary floor: [minimum acceptable]
```

---

## Optional files

These are created automatically by the skills as you use the system. You don't need to create them manually.

| File | Created by | Purpose |
|---|---|---|
| `career_fears.md` | the Mentor, under the memory policy | Candidate or learner-confirmed fears that affect career decisions; sensitive inferences are never auto-promoted |
| `feedback_*.md` | Skills (when you correct them) | Feedback on how skills should behave |
| Any topic-specific memory | Context audit | Facts that shape advice |

---

## How memory gets updated

**Automatically:** the Mentor may save explicit, decision-relevant facts you state. Agent inferences remain candidates until they have independent evidence and you confirm the exact claim.

**Via `/context-audit`:** Runs a structured interview, shows what the system believes and why, and lets you confirm, dispute, correct, retire, or delete memories. Run this after major changes or when a memory feels wrong.

**Manually:** You can edit any memory file directly. They're just Markdown.

---

## Memory file format

All memory files use this frontmatter format:

```markdown
---
name: kebab-case-slug
description: one-line summary — specific enough to decide relevance
metadata:
  type: user | feedback | project | reference
  memory_type: semantic | procedural
  claim_type: explicit | inference | defect | intervention
  status: candidate | confirmed | disputed | retired
  sensitivity: low | medium | high
  created: YYYY-MM-DD
  last_confirmed: YYYY-MM-DD | null
  review_by: YYYY-MM-DD | null
  expires: YYYY-MM-DD | null
  sources:
    - path-or-issue-reference
  consumers:
    - command-or-workflow-name
---

[Memory content]

**Why:** [why this matters]

**How to apply:** [how this should shape advice]
```

Use the complete [memory record template](../examples/memory-record-template.md). Existing files can be migrated when they are next edited; see the [migration guide](memory-policy-migration.md).

When a memory materially changes guidance, log whether the effect was `helpful`, `irrelevant`, `stale`, or `harmful` in `journal/memory-effects.md`.

---

## What NOT to put in memory

- Code patterns or project structure (Claude can read the code)
- Git history (use `git log`)
- In-progress task details (use GitHub Issues)
- Anything already in CLAUDE.md
- One-off emotions recast as lasting traits
- Sensitive inferences you did not explicitly confirm
- Model interpretations presented as your own words

Memory is for facts about *you* — not about the code or the work product.
