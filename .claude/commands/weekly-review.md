Run a weekly review. No input needed — you read everything yourself.

---

## Step 1 — Gather this week's session logs

List all files in `journal/sessions/`. Read each file dated within the last 7 days. If there are no logs, note it and continue.

---

## Step 1.5 — Gather GitHub issue activity this week

Run these queries to capture work that may not have a session log:

```bash
# Everything touched this week (replace the date with the review week's Monday)
gh issue list --repo YOUR_GITHUB_USERNAME/YOUR_REPO --search "updated:>=YYYY-MM-DD" --state all --limit 50 --json number,title,labels,updatedAt,state,closedAt
# Targeted: interview prep
gh issue list --repo YOUR_GITHUB_USERNAME/YOUR_REPO --search "Interview Practice" --state all --limit 20 --json number,title,labels,updatedAt,state
```

For any interview practice issue updated in the past 7 days, read it to see what prep was done, the transcript, and outcome.

Do not skip this step — exam and learn sessions run via skills create GitHub issues, not session logs.

**Deliverable-state verification:** Before stating any specific deliverable is "not written," "unanswered," or "still open," look up its tracking issue's actual state:

```bash
gh issue view <number> --repo YOUR_GITHUB_USERNAME/YOUR_REPO --json state,closedAt,title
```

If the issue is CLOSED, the deliverable is DONE. Issue state is ground truth.

**Pipeline reliability check:**
Read `personal-professional-profile/career/pipeline.md`. For each row in the **Live** table, note any row overdue or due today.

---

## Step 2 — Gather context via parallel readers

Spawn two Explore sub-agents in parallel. Do not read any raw files yourself in this step.

**Agent A — Activity reader:** Read the session log files from Step 1 and the GitHub issue data from Step 1.5. Return a structured bullet summary (≤300 words): what happened, what was said, what wasn't done. Facts only — no interpretation.

**Agent B — Context reader:** Read these files:
- `system/feedback-loop.md` — North Star (Life Vision, Career Goal, Now Goal) — read this first
- `.claude/memory/MEMORY.md` — index; then read all listed memory files
- `personal-professional-profile/learning/learning-plan.md` — including the Spaced Retrieval Schedule table
- `personal-professional-profile/learning/learning-index.md` — read first for a full topic summary
- Deep-read individual progress files **only if**: (a) `last_session` is within the past 7 days, OR (b) the topic has retrieval debt due this week. Do not read all files.

**Stuck-topic scan (from the index — no extra file reads):** Flag any topic where **`Q Correct` is 0 AND `Last Session` is more than 14 days before today** AND status is not `mastered`. Return: topic name, last-session date, days stuck, and the open thread/blocking question.

Return a structured brief (≤200 words): North Star position, retrieval debt due this week, stuck topics, open threads.

Wait for both agents to complete. Step 3 synthesizes **only from these two summaries**.

---

## Step 3 — Synthesize

Before writing anything, read all memory files in `.claude/memory/`. The synthesis is written **in the Mentor's voice**.

Output the issue rename marker on its own line:
`<!-- title: [Review] Week of YYYY-MM-DD -->`

Then produce the review:

```
## Week of YYYY-MM-DD

### The ledger

*Facts only — tight, scannable, complete. No prose, no interpretation. If a line has nothing, omit it.*

**Did this week**
- **Track A (search/career):** [volume + nature in one line — mocks, applications, outreach, drills]
- **Track B (learning):** [study sessions + whether anything was applied]

**Pipeline status**
- [One line per overdue/due-today row: "[Company] follow-up was due [date], no action logged since." Omit entirely if nothing is due.]

**Learning-plan position**

Render the current learning sequence as a table with a status column:

| Wk | Topic/Layer | Status |
|----|------------|--------|
| W23 | [topic] | ✓ complete |
| **W24** | **[topic]** | **→ current** |
| W25 | [topic] | |

*Status key: `✓ complete` = exam pass + concept deployed in real work/answer. `✓ studied, not applied` = exam pass only. `→ current` = in progress. Blank = future.*

→ **Deliverable:** [the current week's specific learning output]

**Retrieval debt**
- List any topic whose "Re-test by" date falls on or before next Sunday, plus anything overdue.
- If nothing is due: "Nothing due — next rep is [topic] on [date]."

**Stuck topics**
- From Agent B: any topic 0/3 correct AND last touched > 14 days ago (not mastered). One line each.

**Open threads**
- Started-not-finished, questions unanswered, anything that should become a GitHub issue.

**Evidence (→ achievement log)**
- Concrete wins or proof points from this week.

---

### the Mentor's read

*Exactly 3 paragraphs, the Mentor's voice, no bullets, no sub-headers.*

- *Each paragraph opens with a short bolded lead phrase (4–8 words) naming the cut, then prose that earns it.*
- *Three cuts, each ≤ 6 sentences.*
- *Never run a cut you can't stand behind. Every diagnosis traces to a fact in the ledger.*
- *Do not repeat last week's cut — either show what changed or escalate.*

*The three lenses:*
- *Your **behavior** — what you repeatedly did or avoided*
- *Your **thinking** — how your reasoning showed up*
- *Your **progress** — graded honestly against the North Star*

---

### Next week

**Top 3 priorities**

*Exactly 3 numbered one-line items, ordered by priority.*

1. [top career/search action this week]
2. [top learning action this week]
3. [third-priority action]

**Orders:**

Name specific tasks, never categories ("drill the margin answer out loud, timed" not "practice interviewing").

**Learning — do these in order:**

1. **Retrieval reps (~[X] min) — no skill, closed-book only**
   [Only include topics that have been taught — a progress file exists with at least one concept marked `[x]`. An untaught topic routes to step 2 (`/learn`) instead.]

   For each qualifying topic, give the exact `/exam` command to run.

2. **Study [→ current layer] — run `/learn`**
   Give the exact command. State the specific concepts the session should cover.

3. **Write the paragraph (~30 min) — the actual deliverable**
   After the `/learn` session, write this without notes. Give the fill-in-the-blank frame:
   > "For [product], I would use [approach] because [reason tied to the product's constraints]. I would not use [alternative] because [specific reason]. The tradeoff I'd be watching is [one concrete tradeoff]."

   Give the exact `/exam apply` command to run.

**The question to sit with:**
*[One uncomfortable question drawn from what the Mentor knows — something not yet answered honestly.]*
```

---

## Step 3.5 — Verify the review

Before writing the file, check:

- [ ] Exactly 3 sections (ledger, the Mentor's read, next week) — no added headers
- [ ] Every "not done" claim was verified against the tracking issue's actual state
- [ ] Every `[Exam]`/`[Learn]` issue that closed this week appears as a win
- [ ] the Mentor's read does not restate a prior review's cut verbatim
- [ ] the Mentor's read: no bullets, no sub-headers, exactly 3 paragraphs, each ≤ 6 sentences
- [ ] Learning table present and correctly maps current week
- [ ] Next week orders: specific tasks, not categories
- [ ] Top 3 priorities block present, exactly 3 numbered lines

If any check fails, regenerate only the failing section and re-check before continuing.

---

## Step 4 — Write the review file

```bash
YEAR=$(date +%Y)
WEEK=$(date +%V)
```

Write the full synthesized content to `journal/reviews/${YEAR}-W${WEEK}.md`. If a file already exists for this week, overwrite it.

---

## Step 5 — Create a GitHub issue

```bash
gh label create "agent:status:done" --color "#0e8a16" --repo YOUR_GITHUB_USERNAME/YOUR_REPO 2>/dev/null || true
ISSUE_URL=$(gh issue create \
  --repo YOUR_GITHUB_USERNAME/YOUR_REPO \
  --title "[Review] Week of MONDAY_DATE" \
  --body-file "journal/reviews/${YEAR}-W${WEEK}.md" \
  --label "agent:status:done,model:{your running model},machine:yourname")
```

Replace `MONDAY_DATE` with the Monday date of the reviewed week (format: `YYYY-MM-DD`).

---

## Step 6 — Update files

| Task | Inputs |
|---|---|
| 1. Learning progress files | Session log entries where a topic was studied |
| 2. Achievement log | Evidence lines from the ledger only |
| 3. Memory admission and review | Session logs from the past 4 weeks + `journal/memory-effects.md` |
| 4. Decisions check | Any decision recorded in this week's session logs |
| 5. Spaced retrieval schedule | `/exam` outcomes from this week |
| 6. Learning-plan alignment | `learning-plan.md` + current week's deliverable row |

**Task details:**

1. **Learning progress files** — for any topic that appeared in session logs this week, update `last_session` date and append a session log entry if missing.
2. **Achievement log** — if the ledger's "Evidence" section has anything concrete, append it to `personal-professional-profile/career/achievement-log.md`.
3. **Memory admission and review** — follow `system/memory-policy.md` and scan session logs from the past 4 weeks.
   - Explicit facts, goals, constraints, and preferences may be confirmed immediately with provenance and a review horizon.
   - Session events remain episodic evidence.
   - Behavioural inferences become candidates only after three independent episodes; repeated summaries count once. Add sources, expiry, and consumers, then seek learner confirmation rather than activating the claim silently.
   - One reproduced workflow defect may justify a procedural correction. Sensitive psychological inferences are never promoted automatically.
   - Review touched memories for contradiction, expiry, provenance, and effects. Do not sweep-migrate untouched legacy records.
   - Read `journal/memory-effects.md`; stop applying stale or harmful memories and flag them for correction, dispute, retirement, or deletion.
4. **Decisions check** — if any session log records a choice the user made, check `journal/decisions/`. If not already logged, create a file and update `journal/decisions/INDEX.md`.
5. **Spaced retrieval schedule** — update the table in `learning-plan.md`. On pass, push "Re-test by" out 2–3 weeks; on miss, reset to ~1 week.
6. **Learning-plan alignment check** — confirm the current week's artifact is still correctly derived from the Career Goal.

---

## Step 7 — Commit and push

```bash
git add journal/reviews/ journal/memory-effects.md .claude/memory/ personal-professional-profile/learning/progress/ personal-professional-profile/learning/learning-plan.md personal-professional-profile/career/achievement-log.md journal/decisions/
git commit -m "weekly review $(date +%Y-W%V)"
git push origin main
```

---

## Step 8 — Close

One sentence: what the week looked like overall. Then:

`_Complexity: ~X input / ~Y output tokens (est.)_`
