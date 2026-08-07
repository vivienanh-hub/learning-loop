# Learning Loop

The learning and career system I run on myself, built on [Claude Code](https://claude.ai/code).

Ten slash commands, five shell scripts, and a memory policy. Nothing compiles — the behaviour is entirely Markdown instructions that Claude reads and follows, with GitHub Issues as the session log.

I've written about why it exists and what it turned out to know about me: **[In order to help me learn, it had to understand me well](https://vivienanh-hub.github.io/2026-08-02-learning-loop/)**. This README is the technical entry point.

---

## The loop

Learning systems don't fail because the teaching is bad. They fail because nothing ever checks — you study, you feel like you understood it, and no part of the process comes back to find out whether that was true.

Four stages, handing off to each other through files on disk.

| Stage | Commands | What happens |
|---|---|---|
| **Learn** | `/lab` `/learn` | A topic is split into concept chunks. You don't advance until three answers are graded correct. |
| **Test** | `/exam` | Closed-book. A separate judge decides Pass or Fail. |
| **Record** | `/weekly-review` `/portfolio-capture` | What happened, what's due for retrieval, what's worth banking as evidence. |
| **Adapt** | `/calibrate` `/goal-review` `/horizon-scan` `/context-audit` | The system inspects itself and the field, and proposes changes to its own instructions. |

---

## Three design decisions

The parts worth stealing, and the reason the repo is public.

**1 · The examiner can't grade its own work.** Every `/exam` attempt spawns a fresh judge that sees only the question, the rubric, and the answer — never the conversation. A model that just finished explaining something reads your answer charitably against its own explanation. Verdicts are binary: "partial" and "almost" are banned in writing, because a hedged verdict is the same as no verdict.
→ [`exam.md`](.claude/commands/exam.md)

**2 · A written policy for what the system may believe about me.** It keeps durable records about how I work. Left unconstrained, an agent turns one bad week into a permanent trait and then advises from it for months. So evidence, inference and intervention stay separate; a behavioural inference needs three *independent* episodes plus my explicit confirmation before it can shape anything; sensitive inferences never auto-promote at any threshold.
→ [`docs/memory-policy.md`](docs/memory-policy.md) · [worked audit](examples/memory-audit-sample.md)

**3 · The system audits its own wiring.** Nine contracts, each naming a signal raised in one place that must land in another. `/calibrate` walks all nine every month and reports the ones that never arrived. The failure mode of every personal system I'd built before this one wasn't a wrong step — it was a handoff that silently stopped happening and went unnoticed for two months.
→ [`calibrate.md`](.claude/commands/calibrate.md) §4.5

---

## What running it surfaced

Findings that only show up once the thing runs unattended, against real work, for months.

**A prompt-level gate is not a fix.** An instruction that sessions rename their own issue was reworded twice, moved to the top of the file, then backed by a stop hook — and still failed six times. The cause was structural: these skills run through a headless watcher the hook never saw. What held was a deterministic check in bash. If correctness depends on the model remembering something, it isn't specified — it's hoped for.

**An evaluator with no ground truth will invent one.** `/exam` on an untaught topic had no answer key, so it produced a plausible rubric and graded against that, with the same binary verdict it uses when the rubric is real. Fixed with a teach-first pass.

**One threshold can't govern four kinds of claim.** The first memory rule promoted any pattern seen three times into a durable belief — collapsing stated facts, events, the system's inferences about me, and decisions to change its own behaviour into a single test. The current policy separates them and requires confirmation for anything inferred. There's a [migration guide](docs/memory-policy-migration.md) because I had to migrate my own records.

---

## What's in the repo

Ten commands. Each is a Markdown file with no code in it — the behaviour is entirely what the prose specifies.

| Command | What it does |
|---|---|
| `/lab` | Brainstorm and pressure-test; names unsupported claims and skipped reasoning on sight |
| `/learn` | Teaches a topic chunk by chunk; three graded-correct answers per chunk before advancing |
| `/exam` | Closed-book Socratic exam with an independent judge; three attempts then back to `/learn` |
| `/weekly-review` | The forcing function. Ledger, honest read, next week's specific orders |
| `/calibrate` | Monthly self-audit: skill usage, memory health, the nine wiring contracts |
| `/goal-review` | Quarterly reconciliation of Life Vision → Career Goal → Now Goal |
| `/horizon-scan` | Monthly outward scan; every signal gets exactly one verdict — Noise, Watch, or Act |
| `/context-audit` | Shows every belief the system holds about me, with source and consumers; confirm, dispute, correct, retire, or delete |
| `/mentor` | Career accountability. Loads history, goals, and recent sessions before speaking |
| `/portfolio-capture` | Captures a win before the detail fades |

Also here: [`scripts/check.py`](scripts/check.py), which is what stops prose from rotting silently — it verifies command references, links, frontmatter, issue-template titles and skill counts, and runs on every push. Plus [`docs/skill-map.md`](docs/skill-map.md) for routing, [`automation/`](automation/) for the scheduler that runs the timed skills headlessly, and [`examples/`](examples/) for real output — a [field scan](examples/horizon-scan-sample.md), an [exam transcript](examples/exam-transcript.md), and a [memory audit](examples/memory-audit-sample.md).

---

## Privacy

Everything runs locally and writes to your own repo; nothing leaves except to Claude, in the normal course of using Claude Code. The [`.gitignore`](.gitignore) excludes memory, session logs, reviews, decisions, and career files by default, on the assumption that a workspace built from this may be public. Every example here is synthetic or fabricated and labelled as such, and the memory policy forbids publishing raw session excerpts.

---

## Fork it

Setup is in [INSTALL.md](INSTALL.md) — you'll need Claude Code, an authenticated `gh` CLI, and a GitHub repo. Expect an hour, and expect to rewrite the tutor voices; they're calibrated to how I like being spoken to, which is probably not how you do. The scheduler in [`automation/`](automation/) is a starting point rather than a hardened one — no retry backoff, no alerting if the watcher dies.

The pieces that transfer without the rest of the system are the [memory policy](docs/memory-policy.md) and the [wiring-contract check](.claude/commands/calibrate.md). Take those.

---

## Built with

[Claude Code](https://claude.ai/code) · GitHub Issues as the session log and work queue · Markdown for everything else. No database, no external services, no vendor lock beyond Claude Code itself.

MIT licensed — see [LICENSE](LICENSE).
