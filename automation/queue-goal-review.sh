#!/bin/bash
# Quarterly goal review auto-queue. Run this once a quarter via cron or a
# LaunchAgent — see automation/README.md. Queues a GitHub issue labeled
# agent:status:todo, and watcher.sh (always running) picks it up and runs
# the full /goal-review skill end to end.

REPO="YOUR_GITHUB_USERNAME/YOUR_REPO"
REPO_DIR="/path/to/your/workspace"
MACHINE_LABEL="machine:yourname"
MODEL_LABEL="model:sonnet"   # which model the watcher runs this skill on
REVIEW_DIR="$REPO_DIR/journal/goal-reviews"

# Sync first — same reason as the other queue scripts: avoid a stale
# file-existence check queueing a duplicate.
git -C "$REPO_DIR" pull --ff-only origin main 2>&1 | sed "s/^/[$(date '+%Y-%m-%d %H:%M:%S')] git pull: /"

YEAR=$(date +%Y)
MONTH=$(date +%-m)
QUARTER=$(( (MONTH - 1) / 3 + 1 ))
THIS_PERIOD="${YEAR}-Q${QUARTER}"

if [ -f "$REVIEW_DIR/$THIS_PERIOD.md" ]; then
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] Goal review for $THIS_PERIOD already exists. Skipping."
  exit 0
fi

EXISTING=$(gh issue list --repo "$REPO" --search "[Goal Review] $THIS_PERIOD in:title" --json number --jq '.[0].number')
if [ -n "$EXISTING" ]; then
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] Goal review issue #$EXISTING for $THIS_PERIOD already queued. Skipping."
  exit 0
fi

ISSUE_URL=$(gh issue create --repo "$REPO" \
  --title "[Goal Review] $THIS_PERIOD" \
  --body "Quarterly automated goal review. Run \`/goal-review\` end to end: read the North Star and goal cascade, the quarter's reviews and horizon scans, challenge each goal level, write \`journal/goal-reviews/$THIS_PERIOD.md\`, commit and push, then close out." \
  --label "$MACHINE_LABEL,$MODEL_LABEL,agent:status:todo")

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Queued goal review for $THIS_PERIOD: $ISSUE_URL"
