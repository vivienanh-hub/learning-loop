---
description: Monthly field scan — every signal triaged Noise / Watch / Act
---

Monthly outward scan of your field. Surfaces what you don't know you don't know, filters it, and routes "Act" signals into the system. Run once a month — not weekly (the field doesn't shift that fast).

---

## Step 1 — Read current context

Read these before scanning. Do not announce it.

- `system/feedback-loop.md` — the current Career Goal and Now Goal (what "relevant" means right now)
- `personal-professional-profile/learning/learning-plan.md` — current gaps and backlog (to know what's already tracked)
- `personal-professional-profile/career/experience.yaml` — your current positioning
- The most recent horizon scan log if one exists: `journal/horizon-scans/` (list files, read the latest)

---

## Step 2 — Scan (three fixed lenses)

Search for recent signal across three lenses. Use web search for each. Keep results tight — 3–5 signals per lens, no more.

**Lens A — How senior roles in your domain are being redefined**
Search: `"[your target role]" job description [current year]` and `[your domain] product manager skills [current year]`
What to look for: skills newly appearing in JDs; anything the role now *requires* that your current positioning doesn't cover.

**Lens B — Capability shifts in your domain**
Search: `[your domain] product management skills [current year]`
What to look for: new concepts entering the senior PM vocabulary; anything that would make your current fluency look dated in 6 months.

**Lens C — What high-signal practitioners are saying**
Search: leading voices in your domain + current year.
What to look for: any major reframe in how senior work is being defined; anything that challenges your current Career Goal framing.

---

## Step 3 — Filter every signal: Noise / Watch / Act

For every signal found, assign exactly one verdict. Be ruthless — most things are Noise or Watch.

| Verdict | Meaning | Action |
|---------|---------|--------|
| **Noise** | Hype, already known, or won't be durable in 12 months | Discard. Name it once so it's not revisited. |
| **Watch** | Real but not urgent; check again in 1–2 months | Note in the scan log under "Watching." |
| **Act** | Changes something *now* — a gap, a positioning move, or a goal question | Route immediately (Step 4). |

---

## Step 4 — Route every "Act" signal

Each "Act" signal goes to exactly one destination:

- **→ `learning-plan.md`** if it surfaces a skill gap not already in the backlog. Add a row with the topic, why it matters, and a candidate resource.
- **→ Positioning / CV note** if it means the market rewards something you have but aren't surfacing. Write a one-line note to add to `career/cv-bullet-bank.md`.
- **→ Goal Review flag** if the signal is large enough to question whether the Career Goal is still pointing at the right thing. Write it as a question for the Mentor.

---

## Step 5 — Write the scan log

Write the full output to `journal/horizon-scans/YYYY-MM.md`. Use this format:

```markdown
# Horizon Scan — YYYY-MM

_Scanned: YYYY-MM-DD_

## Signals reviewed

### Lens A — Role redefinition
- [signal]: [verdict: Noise / Watch / Act] — [one-line reason]
- ...

### Lens B — Capability shifts
- [signal]: [verdict] — [one-line reason]
- ...

### Lens C — Practitioner voices
- [signal]: [verdict] — [one-line reason]
- ...

## Act — routed signals

| Signal | Routed to | Action |
|--------|-----------|--------|
| [signal] | learning-plan / CV / Goal Review flag | [what was added/changed] |

## Watching
- [signal] — check again [month]

## Discarded (noise)
- [signal] — [why]
```

---

## Step 6 — Update routed files

Do not ask for confirmation. Do not narrate.

1. **`learning-plan.md`** — add any new skill gaps to the Learning Backlog.
2. **`career/cv-bullet-bank.md`** — add positioning notes if any Act signals went there.
3. **Goal Review flags** — append them to a section `## Goal Review flags` at the bottom of the latest horizon scan log.

---

## Step 7 — Commit and push

```bash
git add journal/horizon-scans/ personal-professional-profile/learning/learning-plan.md personal-professional-profile/career/cv-bullet-bank.md
git commit -m "horizon scan $(date +%Y-%m)"
git push origin main
```

---

## Step 8 — Close

Two sentences: what the scan found overall, and the single most important "Act" signal. Then:

`_Next scan due: [first Sunday of next month]_`
