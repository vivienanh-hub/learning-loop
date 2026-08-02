# Automation

Without this layer, every skill in School of One is something you have to remember to run. `/horizon-scan` monthly, `/weekly-review` weekly, `/goal-review` quarterly, `/calibrate` monthly — none of that happens unless you open Claude Code and type the command. This folder is the forcing function: a scheduler creates a GitHub issue on a cadence, and a watcher process picks it up and runs the skill headlessly, with no one at the keyboard.

---

## How it works

```
cron / LaunchAgent           watcher.sh                    the skill
      |                          |                              |
      | runs on a schedule       |                              |
      v                          |                              |
queue-*.sh creates ------------->|                              |
a labeled GitHub issue           | polls every 30s for          |
(agent:status:todo)              | agent:status:todo issues     |
                                  |                              |
                                  | picks one up, runs ----------> claude --print
                                  | headlessly                    (the skill runs
                                  |                                end to end)
                                  |<------------------------------|
                                  | posts result as a comment,
                                  | commits any changed files,
                                  | flips label to agent:status:done
```

Two moving parts:

1. **A queue script per skill** (`queue-horizon-scan.sh`, `queue-weekly-review.sh`, `queue-goal-review.sh`, `queue-calibrate.sh`) — each one is idempotent (checks whether this period's output already exists before creating anything) and flags a missed prior run so gaps don't go unnoticed.
2. **`watcher.sh`** — a single long-running process that polls for issues labeled `agent:status:todo` + your machine label, runs the matching skill headlessly via `claude --print`, posts the output as a comment, and commits whatever the skill wrote.

The queue scripts are meant to run on their own schedule (cron or a LaunchAgent); the watcher runs continuously in the background.

---

## Setup

### 1. Fill in the placeholders

Every script has three variables at the top:

```bash
REPO="YOUR_GITHUB_USERNAME/YOUR_REPO"
REPO_DIR="/path/to/your/workspace"
MACHINE_LABEL="machine:yourname"
```

Set them once per script, or refactor into a shared config file if you'd rather not repeat yourself.

### 2. Create the GitHub labels (if you haven't already)

Same labels as [INSTALL.md](../INSTALL.md) step 5 — `agent:status:todo`, `agent:status:doing`, `agent:status:done`, `agent:status:failed`, `model:sonnet`, `machine:yourname`.

### 3. Start the watcher

```bash
chmod +x automation/*.sh
./automation/watcher.sh
```

Leave it running (a terminal tab, a `screen`/`tmux` session, or wrapped in its own LaunchAgent/systemd unit).

### 4. Schedule the queue scripts

**Cron** (cross-platform, simplest to start with):

```cron
# m h dom mon dow   command
0 8 * * 1            /path/to/your/workspace/automation/queue-weekly-review.sh   >> ~/school-of-one-cron.log 2>&1
0 8 1 * *             /path/to/your/workspace/automation/queue-horizon-scan.sh    >> ~/school-of-one-cron.log 2>&1
0 8 1 * *             /path/to/your/workspace/automation/queue-calibrate.sh       >> ~/school-of-one-cron.log 2>&1
0 8 1 1,4,7,10 *      /path/to/your/workspace/automation/queue-goal-review.sh     >> ~/school-of-one-cron.log 2>&1
```

That's: weekly review every Monday 8am, horizon scan + calibrate on the 1st of each month, goal review on the 1st of each quarter. Edit with `crontab -e`.

**LaunchAgent** (macOS alternative — one `.plist` per script, in `~/Library/LaunchAgents/`):

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>com.yourname.horizon-scan</string>
  <key>ProgramArguments</key>
  <array>
    <string>/path/to/your/workspace/automation/queue-horizon-scan.sh</string>
  </array>
  <key>StartCalendarInterval</key>
  <dict>
    <key>Day</key><integer>1</integer>
    <key>Hour</key><integer>8</integer>
    <key>Minute</key><integer>0</integer>
  </dict>
  <key>StandardOutPath</key><string>/tmp/horizon-scan.log</string>
  <key>StandardErrorPath</key><string>/tmp/horizon-scan.log</string>
</dict>
</plist>
```

Load it with `launchctl load ~/Library/LaunchAgents/com.yourname.horizon-scan.plist`.

---

## What this doesn't do

- **It doesn't run `/exam` or `/learn` for you.** Those are pulled, not pushed — you start them when you're actually studying. The Spaced Retrieval Schedule that `/weekly-review` maintains in `learning-plan.md` is what tells you what's due; the weekly review queue script is what guarantees that schedule gets checked even in a week you'd otherwise skip it.
- **It doesn't touch memory or skill files without you.** `/calibrate` always stops and asks before editing anything — the automation only guarantees the report happens on schedule, not that changes get applied unattended.
- **It's a starting point, not a hardened scheduler.** No retry backoff, no alerting if the watcher process dies. If you leave it running for months, you'll probably want to add both.
