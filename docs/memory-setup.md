# Memory Setup

School of One builds a persistent memory of who you are over time. This file explains the memory system and what you need to set up.

---

## How memory works

Claude Code has no persistent memory between conversations by default. School of One solves this with a file-based memory system: structured Markdown files in `.claude/memory/` that are read at the start of relevant sessions.

The skills automatically read these files — you don't need to reference them explicitly.

---

## Required files

### `.claude/memory/MEMORY.md`

The index. Every memory file must have a one-line entry here so future sessions know to load it.

```markdown
- [user_profile.md](user_profile.md) — who you are, how you work
- [job_situation.md](job_situation.md) — current job search status
```

### `.claude/memory/user_profile.md`

Who you are and how you learn. Snape reads this to calibrate his voice. Sheldon reads this to frame explanations.

```markdown
---
name: user-profile
description: Who the user is, how they learn, what they value
metadata:
  type: user
---

Background: [your professional background in 2-3 sentences]
Domain: [your area of expertise]
Learning style: [how you learn best — examples, analogies, depth, etc.]
Working style: [how you prefer to engage with Claude]
Goal: [what you're trying to achieve right now]
```

### `.claude/memory/job_situation.md` (if job-searching)

Current status. Snape uses this to calibrate urgency in every session.

```markdown
---
name: job-situation
description: Current job search status and urgency
metadata:
  type: project
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
| `career_fears.md` | Snape (during sessions) | Patterns the user has revealed that affect career decisions |
| `feedback_*.md` | Skills (when you correct them) | Feedback on how skills should behave |
| Any topic-specific memory | Context audit | Facts that shape advice |

---

## How memory gets updated

**Automatically:** Snape saves new information during sessions whenever you reveal something decision-relevant. He narrates the save briefly, in character.

**Via `/context-audit`:** Runs a structured interview and updates all memory files based on what's changed. Run this after major life or career changes.

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
---

[Memory content]

**Why:** [why this matters]

**How to apply:** [how this should shape advice]
```

---

## What NOT to put in memory

- Code patterns or project structure (Claude can read the code)
- Git history (use `git log`)
- In-progress task details (use GitHub Issues)
- Anything already in CLAUDE.md

Memory is for facts about *you* — not about the code or the work product.
