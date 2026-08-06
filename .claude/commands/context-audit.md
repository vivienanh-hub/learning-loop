Audit Claude's current assumptions about you, interview you to correct them, update memory, and produce a Markdown report with recommendations.

---

## Step 1 — Read all context silently

Before saying anything, read the following. Do not announce that you are reading them.

**Memory files:**
- `.claude/memory/MEMORY.md` — index of all memory files
- Every file listed in that index (read them all)

**Workspace context:**
- `CLAUDE.md` — project instructions and working style
- `journal/decisions/INDEX.md` — past decisions on record
- All session logs in `journal/sessions/` dated within the last 30 days

If any file is missing, continue without it.

---

## Step 2 — Build the assumption table

Silently compile every belief you are currently carrying about the user. Cover:

- **Role & identity** — title, background, expertise level, location
- **Current priorities** — what they are working on and why
- **KPIs** — any metrics or success criteria they have stated
- **Tools & workflows** — active tools, automations, rhythms
- **Job search or career status** — if applicable: urgency, financial situation, targets
- **Anything you may be over-weighting** — beliefs from a single session, unverified claims, outdated state

For each item, record:
- What you believe
- Why you believe it (source: memory file, session log, CLAUDE.md, inference)
- Confidence level (High / Medium / Low)
- Status (Confirmed / Assumption / Possibly outdated / Unknown)

Treat candidate, disputed, retired, and expired memory records as items to audit, not active beliefs. Do not let them frame recommendations during the interview.

Do not show this table to the user yet. Use it to drive the interview.

---

## Step 3 — Interview in rounds

Present the audit as a structured interview. Use `AskUserQuestion` tool with multiple-choice options wherever the answer set is bounded. Ask 2–3 questions per round. Never more than 3.

Run exactly 4 rounds, covering these themes in order:

**Round 1 — Role & identity**
Cover: current role or status, how they position themselves professionally, location.
Flag any assumptions or low-confidence items from Step 2 in this area.

**Round 2 — Priorities & urgency**
Cover: what they are actually focused on right now, urgency level, what has changed since the last session.
Flag items marked "possibly outdated."

**Round 3 — KPIs & work processes**
Cover: how they measure themselves, operating rhythm, structured vs. ad hoc approach.
Flag the Unknown items.

**Round 4 — Tools & workflows**
Cover: which tools are active vs. idle, what Claude is actually used for day-to-day, anything missing from the current picture.

After each round, output a brief summary (3–5 bullets) of what changed or was confirmed. Be specific — "Location confirmed: [city]" not "location noted."

Use plain, direct language. No the Mentor persona. This is a calibration exercise.

---

## Step 4 — Update memory

After the interview is complete, decide memory actions with the learner, then update the files.

**Rules:**
- Follow `system/memory-policy.md`; this audit is the learner-control surface for memory
- Update existing files rather than creating new ones where possible
- Only create a new memory file if genuinely new territory
- Remove or correct beliefs that were wrong
- Do not save ephemeral session state — only durable facts, patterns, and decisions
- For every memory reviewed, show claim type, status, source evidence, last confirmation, review/expiry date, consumers, and the behaviour it changes
- For each memory needing a decision, show a concise row with claim, source, current status, consumers, review/expiry date, and the available actions: `confirm`, `dispute`, `correct`, `retire`, or `delete`. Ask before applying the action; do not infer the learner's choice
- Disputed, retired, and expired memories stop influencing guidance. Deletion removes the durable claim, index entry, and any procedure derived only from it; source episodes remain unless their deletion is also requested
- Keep the learner's words separate from model inference. New behavioural inferences remain candidates until the learner confirms the exact claim

Check `MEMORY.md` before writing any file. If the index entry is stale, update it.

Inspect `journal/memory-effects.md`. Surface stale or harmful effects and confirmed memories whose review dates are overdue.

After the learner chooses, apply the saves silently. Do not narrate each write.

---

## Step 5 — Generate the report

Write a Markdown report and save it to:

```
journal/sessions/YYYY-MM-DD-context-audit.md
```

Use today's date. If a file already exists at that path, append `-2` to the filename.

**Report structure:**

```markdown
# Context & Memory Audit — YYYY-MM-DD

## What we audited
[Short paragraph: what was reviewed and what the interview covered]

## What changed in Claude's understanding

### Major corrections
[Table: Item | Was | Now — only for things that actually changed]

### Confirmed (were correct, now explicit)
[Bullet list]

### New information (not in memory before)
[Bullet list]

### Memory actions
[Table: Memory | Previous status | Action | Reason — include corrections, confirmations, disputes, retirements, and deletions]

## Recommendations: automations and skills to build

### High value — build soon
[Named skill or automation, what it does, why it matters now]

### Medium value — worth planning
[Named skill or automation, what it does, why it matters later]

## What to cut or stop doing
[Specific things: idle tools, passive open threads, habits no longer accurate or useful]

## Context to review again later
[Table: Item | Review trigger | Why]

---
*Audit conducted: YYYY-MM-DD | Memory files updated: [list filenames changed]*
```

Keep each section tight. If a section has nothing to say, write "Nothing this cycle."

---

## Step 6 — Commit and push

```bash
git add journal/sessions/YYYY-MM-DD-context-audit.md .claude/memory/ journal/memory-effects.md
git commit -m "docs: context and memory audit YYYY-MM-DD"
git push
```

Stage only the report, memory records actually changed by this audit, the memory index when changed, and the effects log when changed. Do not stage unrelated files.

---

## Step 7 — Close

Tell the user:
1. Where the report was saved (file path)
2. Which memory files were updated (list them)
3. One sentence on the most significant correction from this audit

Then stop.

---

## Token usage estimate

`_Complexity: ~X input / ~Y output tokens (est.)_`
