# Skill Map

A single-table view of every skill in Learning Loop — what it does, its role in the system, and when to use it.

| Skill | Role in the loop | When to use |
|---|---|---|
| `/lab` | Front door — brainstorm facilitator, inquiry engine, router | When you have an idea to pressure-test, a question to explore, or you're not sure which skill to use |
| `/mentor` | Life coach — career accountability, goal alignment, career strategy | When you want a mentor session on career decisions, job search strategy, or goal direction |
| `/learn` | Teacher — structured lesson on a topic, chunk by chunk, with Q&A | When you want to learn something new systematically |
| `/exam` | Examiner — Socratic test of what you actually know | When you want to verify retention, not just study |
| `/horizon-scan` | Field scanner — monthly outward look at your domain | Once a month: what's moving in the field, what's noise, what requires action |
| `/weekly-review` | Weekly synthesizer — the Mentor's read of your week | End of week: what you did, what you avoided, what's next |
| `/calibrate` | System improver — monthly self-diagnosis and repair | Once a month: is the system still working? what's stale or broken? |
| `/goal-review` | North Star checkpoint — quarterly reconciliation of goals | Quarterly or after a major life event: are your goals still right? |
| `/context-audit` | Memory calibrator — updates the system's model of you | When your situation changes significantly, or when the Mentor feels stale |
| `/interview` | Mock interviewer — graded, JD-aware, coaching feedback | Before any real interview or when preparing for a specific role |
| `/cv-job-match` | Role-fit analyzer — matches your profile to a target JD | When evaluating a role before applying |
| `/portfolio-capture` | Achievement logger — captures a win before the details fade | Right after something notable happens: strong interview, shipped feature, key decision |

---

## System map

```
Learning loop:
  /learn → /exam → /weekly-review (ledger) → /calibrate (health check)

Career loop:
  /horizon-scan → /goal-review → /mentor → /interview → /cv-job-match → /portfolio-capture

Monthly loops:
  /horizon-scan (outward)
  /calibrate (inward)

Quarterly:
  /goal-review
```

## Routing logic

- **Have an idea to explore?** → `/lab`
- **Want to learn something?** → `/lab` routes to `/learn`, or call `/learn` directly
- **Want to test retention?** → `/exam [topic]`
- **Preparing for an interview?** → `/interview [JD URL or #issue]`
- **Evaluating a role?** → `/cv-job-match [JD URL]`
- **Career question or feeling stuck?** → `/mentor`
- **End of week?** → `/weekly-review`
- **Something just went well?** → `/portfolio-capture`
- **Monthly field check?** → `/horizon-scan`
- **Monthly system check?** → `/calibrate`
- **Quarterly goal check?** → `/goal-review`
