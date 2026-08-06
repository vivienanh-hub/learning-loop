# [YOUR NAME]'s PM Workspace

Personal workspace for a [YOUR ROLE]. Uses GitHub Issues as a task queue and Claude Code skills for structured PM work.

## Working style

[Replace with your background — e.g. "User has a business background, 5 years in PM. Prefer conceptual explanations with practical examples. Explain trade-offs, not just mechanics."]

## Memory

Domain-specific rules and context live in modular memory files at `.claude/memory/`. Check `.claude/memory/MEMORY.md` for the index before starting any task.

**IMPORTANT — memory write path:** Write all memory files to `.claude/memory/` in this repo, not to any global Claude Code memory location. This repo path is the source of truth.

Follow `system/memory-policy.md` for every memory write. Explicit facts require provenance and review dates; behavioural inferences remain candidates until independently evidenced and confirmed by the learner. Candidate, disputed, retired, and expired memories must not shape guidance.

Note: the shipped `.gitignore` excludes `.claude/memory/`, since memory holds personal detail and this template assumes a public repo. Your memory persists on disk either way. If your workspace repo is private and you want memory backed up and synced across machines, drop that line from `.gitignore`.

## Self-improving rules

- Before starting a task, review existing rules in memory.
- Apply confirmed rules by default without asking.
- After receiving feedback on your approach, update the relevant memory file.

## LinkedIn URLs

LinkedIn recommended-feed URLs require a login and cannot be fetched. Direct job view URLs (`/jobs/view/[ID]`) are publicly accessible.

When a LinkedIn URL contains a `currentJobId` query parameter, extract the ID and rewrite the URL to `https://www.linkedin.com/jobs/view/{id}` before fetching.

## Session capture

At the end of every substantive conversation (3+ meaningful turns), write a session log to `journal/sessions/YYYY-MM-DD-HHMM.md`.

**Format:**

```markdown
# Session: YYYY-MM-DD HH:MM

## What we covered
- bullet per topic or task

## What clicked / was decided
- insights, conclusions, or choices made

## Evidence worth saving
- any wins, outputs, or proof points

## Open threads
- anything unresolved or worth continuing next time
```

Skip the log if the conversation was fewer than 3 meaningful turns.
