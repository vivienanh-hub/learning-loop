#!/bin/bash
# Weekly review auto-queue. Run this once a week via cron or a LaunchAgent
# — see automation/README.md. Queues a GitHub issue labeled agent:status:todo,
# and watcher.sh (always running) picks it up and runs the full
# /weekly-review skill end to end.
#
# This is the review that maintains the Spaced Retrieval Schedule in
# learning-plan.md — pushing "re-test by" dates out on a pass, pulling them
# in on a miss. Automating the trigger is what keeps that schedule honest
# instead of drifting whenever a week gets busy.

REPO="YOUR_GITHUB_USERNAME/YOUR_REPO"
REPO_DIR="/path/to/your/workspace"
MACHINE_LABEL="machine:yourname"
REVIEW_DIR="$REPO_DIR/journal/reviews"

# Sync first — a review can complete via a session that isn't this local
# clone, leaving the file-existence check below stale and queueing a
# duplicate.
git -C "$REPO_DIR" pull --ff-only origin main 2>&1 | sed "s/^/[$(date '+%Y-%m-%d %H:%M:%S')] git pull: /"

YEAR=$(date +%Y)
WEEK=$(date +%V)
THIS_PERIOD="${YEAR}-W${WEEK}"
PREV_YEAR=$(date -v-7d +%Y 2>/dev/null || date -d "-7 days" +%Y)
PREV_WEEK=$(date -v-7d +%V 2>/dev/null || date -d "-7 days" +%V)
PREV_PERIOD="${PREV_YEAR}-W${PREV_WEEK}"

if [ -f "$REVIEW_DIR/$THIS_PERIOD.md" ]; then
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] Weekly review for $THIS_PERIOD already exists. Skipping."
  exit 0
fi

EXISTING=$(gh issue list --repo "$REPO" --search "[Review Trigger] $THIS_PERIOD in:title" --json number --jq '.[0].number')
if [ -n "$EXISTING" ]; then
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] Weekly review issue #$EXISTING for $THIS_PERIOD already queued. Skipping."
  exit 0
fi

MISSED_NOTE=""
if [ ! -f "$REVIEW_DIR/$PREV_PERIOD.md" ]; then
  MISSED_NOTE="

**Missed-run flag:** \`journal/reviews/$PREV_PERIOD.md\` does not exist. The previous week's review may not have completed — check for a stuck \`[Review]\` issue for that week before proceeding."
fi

ISSUE_URL=$(gh issue create --repo "$REPO" \
  --title "[Review Trigger] $THIS_PERIOD" \
  --body "Weekly automated review. Run \`/weekly-review\` end to end: gather session logs and issue activity, synthesize, verify against the rubric, write the journal file, update the Spaced Retrieval Schedule in learning-plan.md, commit and push, then close out.${MISSED_NOTE}" \
  --label "$MACHINE_LABEL,model:sonnet,agent:status:todo")

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Queued weekly review for $THIS_PERIOD: $ISSUE_URL"
