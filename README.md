# Learning Loop

The learning and career system I run on myself, built on [Claude Code](https://claude.ai/code).

I built it because I kept studying things and couldn't tell, three weeks later, whether I had actually learned them. It has run every week since, without a gap.

This repo is the system itself, published as a worked example of what it takes to specify agent behaviour when the agent has to make judgments about a person. It is not a product and there is nothing you need to install — see [Fork it](#fork-it) at the end if you want to.

---

## What it has actually done

Numbers from my own instance, which is private. These describe activity, not outcomes — I can show that the loop ran, not that it made me smarter.

| | |
|---|---|
| Weekly reviews | 11 consecutive, W21–W31, no gaps |
| Topics taught | 15 |
| Exams sat | 11 |
| Monthly field scans | 3 |
| Quarterly goal reviews | 3 |
| Memory records under the policy below | 39 |
| Sessions logged as GitHub issues | 220 |

The unbroken weekly-review streak is the number I care about. Everything else in the system is optional in any given week; that one is the forcing function, and it held through weeks when nothing else did.

---

## The problem it solves

Learning systems don't fail because the teaching is bad. They fail because nothing ever checks. You study, you feel like you understood it, and no part of the process ever comes back to find out whether that was true. The same is true of career intent: goals get set once and then quietly stop matching what you're actually doing.

So the system is built as four stages that hand off to each other through files on disk. Each stage writes something the next one reads.

| Stage | Commands | What happens |
|---|---|---|
| **Learn** | `/lab` `/learn` | A topic is split into concept chunks. You don't advance until three answers are graded correct. |
| **Test** | `/exam` `/interview` | Closed-book. A separate judge decides Pass or Fail. |
| **Record** | `/weekly-review` `/portfolio-capture` | What actually happened, what's due for retrieval, what's worth banking as evidence. |
| **Adapt** | `/calibrate` `/goal-review` `/horizon-scan` `/context-audit` | The system inspects itself and the field, and proposes changes to its own instructions. |

---

## Three design decisions

These are the parts worth stealing, and the reason the repo is public.

### 1. The examiner can't grade its own work

Every `/exam` attempt spawns a fresh judge sub-agent that sees only the question, the rubric, and the answer verbatim. It never sees the conversation.

A model that just finished explaining something is the worst possible judge of whether you learned it — the explanation is sitting in its context, and it will read your answer charitably against it. Separating the judge is the cheapest fix.

The verdict is binary. Pass or Fail. "Partial" and "almost" are banned in writing, because a hedged verdict is the same as no verdict.

→ [`exam.md`](.claude/commands/exam.md), [`learn.md`](.claude/commands/learn.md)

### 2. A written policy for what the system is allowed to believe about me

The system keeps durable records about how I work and what I avoid. Left unconstrained, an agent will turn one bad week into a permanent trait and then quietly advise you from it for months.

So there's a policy, and the tutors are bound by it:

- **Evidence, inference, and intervention stay separate.** An observed event is not a claim about me. A claim about me is not a decision to change how the system behaves.
- **A behavioural inference needs three *independent* episodes plus my explicit confirmation** before it can shape guidance. Copies and summaries of the same event count once.
- **Sensitive inferences — psychological, health, identity — never auto-promote at any threshold.**
- **A candidate memory cannot change another tutor's behaviour.** Unconfirmed means inert, not "slightly weighted."
- **Every record states how it can be falsified** and when it expires.
- **Effects are measured on my outcome, not on successful recall.** A tutor repeating a pattern label back at me is not evidence the pattern was useful.

→ [`docs/memory-policy.md`](docs/memory-policy.md) · [worked audit example](examples/memory-audit-sample.md)

### 3. The system audits its own wiring

Nine contracts, each naming a signal raised in one place that must land in another — a horizon-scan `Act` row must reach the learning backlog; a weekly-review evidence line must reach the achievement log; a decision recorded in a review must reach the decisions log.

`/calibrate` walks all nine every month and reports the ones that never arrived.

The failure mode of every personal system I've built before this one wasn't that a step was wrong. It was that a handoff silently stopped happening and nothing noticed for two months.

→ [`calibrate.md`](.claude/commands/calibrate.md) §4.5

---

## What's in the repo

Twelve commands. Each is a Markdown file with no code in it — the behaviour is entirely what the prose specifies.

| Command | What it does |
|---|---|
| `/lab` | Brainstorm and pressure-test; names unsupported claims and skipped reasoning on sight |
| `/mentor` | Career accountability. Loads history, goals, and recent sessions before speaking; diagnoses before prescribing |
| `/learn` | Teaches a topic chunk by chunk; three graded-correct answers per chunk before advancing |
| `/exam` | Closed-book Socratic exam with an independent judge; three attempts then back to `/learn` |
| `/weekly-review` | The forcing function. Ledger, honest read, next week's specific orders |
| `/calibrate` | Monthly self-audit: skill usage, memory health, the nine wiring contracts |
| `/goal-review` | Quarterly reconciliation of Life Vision → Career Goal → Now Goal, with a promotion-readiness score |
| `/horizon-scan` | Monthly outward scan; every signal gets exactly one verdict — Noise, Watch, or Act |
| `/context-audit` | Shows every belief the system holds about me, with source and consumers; confirm, dispute, correct, retire, or delete |
| `/interview` | Mock interview from a real job description, scored, with a model answer built from my own CV |
| `/cv-job-match` | Role-fit analysis: gaps, pitch angle, what to fix before applying |
| `/portfolio-capture` | Captures a win before the detail fades |

Also here: [`docs/skill-map.md`](docs/skill-map.md) for routing, [`automation/`](automation/) for the scheduler that runs the timed skills headlessly, and [`examples/`](examples/) for real output — a [field scan](examples/horizon-scan-sample.md), an [exam transcript](examples/exam-transcript.md), and a [memory audit](examples/memory-audit-sample.md).

---

## What I got wrong

**The memory rule was too blunt for the first two months.** The original version promoted any pattern seen three times into a durable belief. That collapsed four different things — facts I'd stated, events that happened, the system's interpretations of me, and decisions to change tutor behaviour — into one threshold. It meant a rough fortnight could harden into "you avoid applied work" and then get quoted back at me as though I'd said it. The current policy separates those and requires confirmation for anything inferred. There's a [migration guide](docs/memory-policy-migration.md) because I had to migrate my own records.

**I built both halves at once.** The learning loop and the career loop went in together. I should have proven one closed before starting the other — the first six weeks had more surface area than evidence.

**I hand-built a router the platform already provides.** `/lab` used to carry a table telling you which other skill to call. It only ever knew half the system, it went stale twice, and at one point it routed to a command that had never existed. Claude Code's own `/` menu does the job properly the moment each command declares a `description` — which none of mine did. The table is gone and the descriptions are the fix.

**Setup is still too long.** Eight steps, a hand-run `sed`, and eight label-creation commands. It works, and it's more friction than it should be.

**The scheduler is a starting point, not a hardened one.** No retry backoff, no alert if the watcher process dies, and concurrent runs can contend over the same git working tree.

---

## Privacy

Everything runs locally and writes to your own repo. Nothing is sent anywhere except to Claude, in the normal course of using Claude Code.

The [`.gitignore`](.gitignore) here excludes memory, session logs, reviews, decisions, CV, and job-search pipeline by default, on the assumption that a workspace built from this template may be public. My own instance is private regardless.

Every example in this repo is synthetic or fabricated and labelled as such. The memory policy explicitly forbids publishing raw session excerpts or personal memory records.

---

## Fork it

If you want to run it: [INSTALL.md](INSTALL.md). You'll need Claude Code, an authenticated `gh` CLI, and a GitHub repo. Expect to spend an hour on setup and to rewrite the tutor voices — they're calibrated to how I like being spoken to, which is probably not how you do.

The pieces that transfer without the rest of the system are the [memory policy](docs/memory-policy.md) and the [wiring-contract check](.claude/commands/calibrate.md). Take those.

---

## Built with

[Claude Code](https://claude.ai/code) · GitHub Issues as the session log and work queue · Markdown files for everything else. No database, no external services, no vendor lock beyond Claude Code itself.

MIT licensed — see [LICENSE](LICENSE).
