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
cp -r school-of-one/.claude/commands/ your-workspace/.claude/commands/
```

Or fork this repo and work directly inside it.

### 2. Set up your CLAUDE.md

Copy [examples/CLAUDE-starter.md](examples/CLAUDE-starter.md) to your repo root as `CLAUDE.md` and fill in the fields marked `[YOUR_...]`.

This file tells Claude what kind of learner you are, where your files live, and how to behave across sessions.

### 3. Create the folder structure

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
│   └── goal-reviews/
├── system/
│   └── feedback-loop.md
└── cv/
    └── your_cv.tex        ← or .pdf, .md — update the path in cv-job-match.md and interview.md
```

### 4. Fill in the key files

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

**`personal-professional-profile/career/experience.yaml`** — your work history. Used by Snape, the interview skill, and cv-job-match.

**`.claude/memory/user_profile.md`** — how you learn, your background, your working style. Start with what you know about yourself and let the system refine it over time.

### 5. Create GitHub issue labels

The skills use GitHub issue labels for workflow state. Create these in your repo:

```bash
gh label create "agent:status:todo" --color "#e11d48" --repo YOUR_GITHUB_USERNAME/YOUR_REPO
gh label create "agent:status:doing" --color "#f97316" --repo YOUR_GITHUB_USERNAME/YOUR_REPO
gh label create "agent:status:done" --color "#16a34a" --repo YOUR_GITHUB_USERNAME/YOUR_REPO
gh label create "model:sonnet" --color "#6366f1" --repo YOUR_GITHUB_USERNAME/YOUR_REPO
gh label create "model:opus" --color "#8b5cf6" --repo YOUR_GITHUB_USERNAME/YOUR_REPO
gh label create "machine:yourname" --color "#94a3b8" --repo YOUR_GITHUB_USERNAME/YOUR_REPO
```

### 6. Run your first session

Open Claude Code in your workspace and try:

```
/sheldon what does it mean to be an AI product manager in 2026?
```

Or if you want to learn a topic:

```
/learn RAG and vector search
```

Or sit an exam on something you already know:

```
/exam jobs-to-be-done
```

---

## Adapting the skills

Every skill is a Markdown file you own. Change the voice, adjust the rubric, add your own file paths. The skills are instructions — they do exactly what they say.

The most important file to adapt: `snape.md`. His opening provocation reads from your session logs and career memory. The better your memory files, the sharper he gets.
