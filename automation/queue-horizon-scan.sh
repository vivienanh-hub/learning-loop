#!/bin/bash
# Monthly horizon scan auto-queue. Run this once a month via cron or a
# LaunchAgent — see automation/README.md. It queues a GitHub issue labeled
# agent:status:todo, and watcher.sh (always running) picks it up and runs
# the full /horizon-scan skill end to end with no human input.

REPO="YOUR_GITHUB_USERNAME/YOUR_REPO"
REPO_DIR="/path/to/your/workspace"
MACHINE_LABEL="machine:yourname"
SCAN_DIR="$REPO_DIR/journal/horizon-scans"

# Sync first — a scan can complete via a session that isn't this local
# clone, leaving the file-existence check below stale and queueing a
# duplicate.
git -C "$REPO_DIR" pull --ff-only origin main 2>&1 | sed "s/^/[$(date '+%Y-%m-%d %H:%M:%S')] git pull: /"

MONTH=$(date +%Y-%m)
PREV_MONTH=$(date -v-1m +%Y-%m 2>/dev/null || date -d "-1 month" +%Y-%m)

if [ -f "$SCAN_DIR/$MONTH.md" ]; then
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] Horizon scan log for $MONTH already exists. Skipping."
  exit 0
fi

EXISTING=$(gh issue list --repo "$REPO" --search "[Horizon Scan] $MONTH in:title" --json number --jq '.[0].number')
if [ -n "$EXISTING" ]; then
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] Horizon scan issue #$EXISTING for $MONTH already queued. Skipping."
  exit 0
fi

MISSED_NOTE=""
if [ ! -f "$SCAN_DIR/$PREV_MONTH.md" ]; then
  MISSED_NOTE="

**Missed-run flag:** \`journal/horizon-scans/$PREV_MONTH.md\` does not exist. Last month's horizon scan may not have completed — check for a stuck \`[Horizon Scan] $PREV_MONTH\` issue before proceeding."
fi

ISSUE_URL=$(gh issue create --repo "$REPO" \
  --title "[Horizon Scan] $MONTH" \
  --body "Monthly automated horizon scan. Run \`/horizon-scan\` and follow it end to end: scan the field, filter every signal Noise/Watch/Act, route Act signals, write the journal log, commit and push, then close out.${MISSED_NOTE}" \
  --label "$MACHINE_LABEL,model:sonnet,agent:status:todo")

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Queued horizon scan for $MONTH: $ISSUE_URL"
