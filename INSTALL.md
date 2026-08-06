# Installation

## Prerequisites

1. A [GitHub account](https://github.com) with a repository for your workspace
2. [Claude Code](https://claude.ai/code) installed and authenticated
3. The `gh` CLI installed and authenticated (`gh auth login`)

---

## Setup

### 1. Copy the skill library

Copy the `.claude/commands/` folder from this repo into your workspace repo:

```bash
cp -r learning-loop/.claude/commands/ your-workspace/.claude/commands/
```

Or fork this repo and work directly inside it.

### 2. Point the skills at your repo

The skills shell out to `gh` directly, and they ship with a placeholder repo. Replace it in the copied files:

```bash
cd your-workspace/.claude/commands
sed -i '' 's|YOUR_GITHUB_USERNAME/YOUR_REPO|your-username/your-repo|g' *.md   # macOS
sed -i    's|YOUR_GITHUB_USERNAME/YOUR_REPO|your-username/your-repo|g' *.md   # Linux
```

Nine of the twelve skills reference the repo this way — `/lab`, `/mentor`, `/learn`, `/exam`, `/weekly-review`, `/calibrate`, `/interview`, `/cv-job-match`, `/portfolio-capture`. Skip this step and each one fails on its first `gh` call. (`/context-audit`, `/goal-review`, and `/horizon-scan` are file-only and need no change.)

The automation scripts carry the same placeholder plus two more — see [automation/README.md](automation/README.md) step 1.

### 3. Set up your CLAUDE.md

Copy [examples/CLAUDE-starter.md](examples/CLAUDE-starter.md) to your repo root as `CLAUDE.md` and fill in the fields marked `[YOUR_...]`.

This file tells Claude what kind of learner you are, where your files live, and how to behave across sessions.

### 4. Create the folder structure

The skills expect this layout (create folders, leave files empty for now):

```
your-workspace/
├── CLAUDE.md
├── .claude/
│   ├── commands/          ← the skills from this repo
│   └── memory/
│       ├── MEMORY.md      ← memory index (start empty)
│       └── user_profile.md
├── personal-professional-profile/
│   ├── career/
│   │   ├── experience.yaml
│   │   ├── achievement-log.md
│   │   ├── cv-bullet-bank.md
│   │   └── pipeline.md
│   ├── learning/
│   │   ├── learning-plan.md
│   │   ├── learning-index.md
│   │   └── progress/
│   └── interview-prep/
│       └── story-bank/
├── journal/
│   ├── sessions/
│   ├── reviews/
│   ├── horizon-scans/
│   ├── decisions/
│   ├── goal-reviews/
│   ├── memory-effects.md
│   └── system-health/
├── system/
│   ├── feedback-loop.md
│   └── memory-policy.md  ← copy from docs/memory-policy.md
└── cv/
    └── your_cv.tex        ← or .pdf, .md — update the path in cv-job-match.md and interview.md
```

### 5. Fill in the key files

**`system/feedback-loop.md`** — your goal cascade. The skills read this constantly to keep advice anchored. Minimum structure:

```markdown
# North Star

## Life Vision
[What you're building toward — the life you want the career to fund]

## Career Goal
[Your 3-year career target: role, domain, impact]

## Now Goal
[Your current concrete target: specific role/company type, salary, timeline]
```

**`personal-professional-profile/career/experience.yaml`** — your work history. Used by the Mentor, the interview skill, and cv-job-match.

**`.claude/memory/user_profile.md`** — how you learn, your background, your working style. Start with what you know about yourself and let the system refine it over time.

**`system/memory-policy.md`** — copy [docs/memory-policy.md](docs/memory-policy.md) here. It governs what the skills may remember, how inferences earn confirmation, and how memories expire or are corrected.

**`journal/memory-effects.md`** — create the outcome table shown in the memory policy. Keep this private; it can reveal which memories influenced real decisions.

### 6. Create GitHub issue labels

The skills use GitHub issue labels for workflow state. Create these in your repo:

```bash
gh label create "agent:status:todo" --color "#e11d48" --repo YOUR_GITHUB_USERNAME/YOUR_REPO
gh label create "agent:status:doing" --color "#f97316" --repo YOUR_GITHUB_USERNAME/YOUR_REPO
gh label create "agent:status:done" --color "#16a34a" --repo YOUR_GITHUB_USERNAME/YOUR_REPO
gh label create "agent:status:failed" --color "#7f1d1d" --repo YOUR_GITHUB_USERNAME/YOUR_REPO
gh label create "model:sonnet" --color "#6366f1" --repo YOUR_GITHUB_USERNAME/YOUR_REPO
gh label create "model:opus" --color "#8b5cf6" --repo YOUR_GITHUB_USERNAME/YOUR_REPO
gh label create "model:haiku" --color "#22d3ee" --repo YOUR_GITHUB_USERNAME/YOUR_REPO
gh label create "machine:yourname" --color "#94a3b8" --repo YOUR_GITHUB_USERNAME/YOUR_REPO
```

Then copy the issue templates. `/lab` reads the default `Lab:` title as its rename trigger, and `/interview` reads the **Practice focus** and **Custom focus** fields — both misbehave without them:

```bash
cp -r learning-loop/.github/ISSUE_TEMPLATE/ your-workspace/.github/ISSUE_TEMPLATE/
```

The templates default to `model:sonnet`. Change that in each `.yml` if you run a different model by default.

### 7. Run your first session

Open Claude Code in your workspace and try:

```
/lab what does it mean to be an AI product manager in 2026?
```

Or if you want to learn a topic:

```
/learn RAG and vector search
```

Or sit an exam on something you already know:

```
/exam jobs-to-be-done
```

### 8. Optional: automate the cadence

The skills above run when you type them. `/horizon-scan`, `/weekly-review`, `/goal-review`, and `/calibrate` are meant to run on a schedule — monthly, weekly, quarterly, monthly — and nothing enforces that unless you remember to.

[automation/](automation/) has a queue script per skill plus a watcher process: a cron job or LaunchAgent creates a labeled GitHub issue on schedule, the watcher picks it up and runs the skill headlessly, and the result gets posted and committed with no one at the keyboard. See [automation/README.md](automation/README.md) for setup.

---

## Adapting the skills

Every skill is a Markdown file you own. Change the voice, adjust the rubric, add your own file paths. The skills are instructions — they do exactly what they say.

The most important file to adapt: `mentor.md`. Its opening provocation reads from your session logs and career memory. The better your memory files, the sharper it gets.
