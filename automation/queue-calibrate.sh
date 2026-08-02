#!/bin/bash
# Monthly calibrate auto-queue. Run this once a month via cron or a
# LaunchAgent — see automation/README.md. Queues a GitHub issue labeled
# agent:status:todo, and watcher.sh (always running) picks it up and runs
# the full /calibrate skill end to end. Calibrate still stops and waits for
# a human answer before editing any memory or skill files — this automation
# only guarantees the report and log line happen on schedule.

REPO="YOUR_GITHUB_USERNAME/YOUR_REPO"
REPO_DIR="/path/to/your/workspace"
MACHINE_LABEL="machine:yourname"
LOG_FILE="$REPO_DIR/journal/system-health/log.md"

# Sync first — same reason as the other queue scripts: avoid a stale
# file-existence check queueing a duplicate.
git -C "$REPO_DIR" pull --ff-only origin main 2>&1 | sed "s/^/[$(date '+%Y-%m-%d %H:%M:%S')] git pull: /"

MONTH=$(date +%Y-%m)
PREV_MONTH=$(date -v-1m +%Y-%m 2>/dev/null || date -d "-1 month" +%Y-%m)

if [ -f "$LOG_FILE" ] && grep -q "^## $MONTH" "$LOG_FILE" 2>/dev/null; then
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] Calibrate log entry for $MONTH already exists. Skipping."
  exit 0
fi

EXISTING=$(gh issue list --repo "$REPO" --search "[Calibrate] $MONTH in:title" --json number --jq '.[0].number')
if [ -n "$EXISTING" ]; then
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] Calibrate issue #$EXISTING for $MONTH already queued. Skipping."
  exit 0
fi

MISSED_NOTE=""
if [ -f "$LOG_FILE" ] && ! grep -q "^## $PREV_MONTH" "$LOG_FILE" 2>/dev/null; then
  MISSED_NOTE="

**Missed-run flag:** No entry for $PREV_MONTH in \`journal/system-health/log.md\`. Last month's calibrate run may not have completed — check before proceeding."
fi

ISSUE_URL=$(gh issue create --repo "$REPO" \
  --title "[Calibrate] $MONTH" \
  --body "Monthly automated system-health pass. Run \`/calibrate\` end to end: load context, tally skill usage, find what's stale or broken, print the report, then ask which changes to execute and wait for the answer. Regardless of the answer, append one line to \`journal/system-health/log.md\` before closing.${MISSED_NOTE}" \
  --label "$MACHINE_LABEL,model:sonnet,agent:status:todo")

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Queued calibrate run for $MONTH: $ISSUE_URL"
