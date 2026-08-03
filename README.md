# Learning Loop

An AI-powered learning system that closes its own loop. Built on [Claude Code](https://claude.ai/code).

Not a course. Not a Notion dashboard. A loop — you learn something, you get tested on it cold, the system records what you forgot and what you keep doing, and the next cycle is shaped by both.

---

## What it is

Learning Loop is a set of Claude Code slash commands that give you a structured learning and career development system inside your own repository. Every session is a GitHub Issue. Every agent is a custom skill you own and can modify.

The system compounds: it builds memory of how you learn, tracks your gaps, and adapts to your goals over time.

---

## The loop

### Tutors

- **`/sheldon`** — Front door of the system. Runs brainstorming sessions, tests your reasoning, routes you to the right learning mode. Precise and structured, zero patience for vague thinking.
- **`/snape`** — Life coach and career advisor. Demands honesty, catches when your goals have drifted, asks the questions you've been avoiding.

### The learning cycle

- **`/learn`** — Structured teaching sessions on any topic. Teaches, tests, and tracks what you've covered. Never moves to the next concept until you've demonstrated the last one.
- **`/exam`** — Socratic exam engine. Won't give you the answer. Probes until it finds the edge of what you actually know vs. what you think you know.
- **`/weekly-review`** — Weekly synthesis: what you did, what you avoided, what's next. Written in Snape's voice so it stays honest.

### The pattern layer

- **`/calibrate`** — Monthly system self-improvement run. Reads all your session logs and memory, finds what's stale or broken, and proposes updates. The loop gets better at teaching you over time.
- **`/context-audit`** — Structured interview that updates the system's model of who you are. Run after major changes in your work or goals.
- **`/goal-review`** — Quarterly north star checkpoint. Snape asks whether your goals are still right, still ambitious enough, still connected to the life you said you wanted.
- **`/horizon-scan`** — Monthly outward field scan. Surfaces what's moving in your domain, filters noise from signal (Act / Watch / Noise triage).

### Career

- **`/interview`** — Graded mock interview. Pulls from a real job description. Gives coaching feedback after each answer, with a model answer using your own experience.
- **`/cv-job-match`** — Matches your profile against a target role. Returns gaps, pitch angle, and what to fix before applying.
- **`/portfolio-capture`** — Captures a win into your achievement log while the details are still fresh.

---

## Who it's for

Any serious learner in a fast-moving field. The system was built for AI product management but the architecture is domain-neutral. The tutors, exam engine, pattern memory, and goal reviews apply to anything you're learning at depth.

The prerequisite: you take your own learning seriously enough to design a system for it.

---

## How to use it

See [INSTALL.md](INSTALL.md) for setup.

See [docs/skill-map.md](docs/skill-map.md) for a table of every skill, its role, and when to use it.

See [examples/CLAUDE-starter.md](examples/CLAUDE-starter.md) for a minimal CLAUDE.md to get started.

See [docs/memory-setup.md](docs/memory-setup.md) for the memory layer — what the skills read, and what you need to create.

See [examples/exam-transcript.md](examples/exam-transcript.md) and [examples/horizon-scan-sample.md](examples/horizon-scan-sample.md) for what the skills actually produce.

See [issue #1](https://github.com/vivienanh-hub/learning-loop/issues/1) for what a session actually looks like as a GitHub issue — labels, title, and the comment thread as it progresses from question to verdict. (Fabricated example, not a real session.)

See [issue #2](https://github.com/vivienanh-hub/learning-loop/issues/2) for a weekly review that promotes a one-off note into a tracked pattern. (Fabricated example, not a real review.)

See [automation/](automation/) for the optional scheduler — a queue script per skill plus a watcher that runs `/horizon-scan`, `/weekly-review`, `/goal-review`, and `/calibrate` on their intended cadence with no one at the keyboard.

---

## Built with

- [Claude Code](https://claude.ai/code) — Anthropic's agentic coding tool
- GitHub Issues — task queue and session log
- Markdown files — memory, learning log, and career tracking

No external databases. No paid services beyond Claude Code itself. Everything lives in your repo.
