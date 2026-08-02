#!/bin/bash
# GitHub Issues watcher — runs Claude Code headlessly against issues queued
# with the label agent:status:todo. This is what turns a queued issue (from
# a cron job, a LaunchAgent, or you manually creating one) into an actual
# skill run with no one at the keyboard.
#
# Usage: ./automation/watcher.sh
# Stop:  Ctrl+C (or kill the background process)

REPO="YOUR_GITHUB_USERNAME/YOUR_REPO"
REPO_DIR="/path/to/your/workspace"
MACHINE_LABEL="machine:yourname"
POLL_INTERVAL=30  # seconds between polls

# Singleton lock — exit immediately if another instance is already running.
# Lives under $HOME (not /tmp) since some OSes periodically sweep /tmp
# entries that haven't been accessed in a few days, which would silently
# delete the lock out from under a long-running process.
LOCKDIR="$HOME/.school-of-one-watcher.lock.d"
LOCKPID="$LOCKDIR/pid"

if [ -d "$LOCKDIR" ]; then
  if [ -f "$LOCKPID" ] && kill -0 "$(cat "$LOCKPID")" 2>/dev/null; then
    echo "[watcher] Already running (pid $(cat "$LOCKPID")). Exiting."
    exit 1
  fi
  echo "[watcher] Stale lock from pid $(cat "$LOCKPID" 2>/dev/null). Reclaiming."
  rm -rf "$LOCKDIR"
fi

mkdir "$LOCKDIR" || { echo "[watcher] Failed to acquire lock. Exiting."; exit 1; }
echo $$ > "$LOCKPID"
trap 'rm -rf "$LOCKDIR"' EXIT

run_issue() {
  local ISSUE_NUM=$1

  echo "[$(date '+%H:%M:%S')] Picking up issue #$ISSUE_NUM"

  HARNESS_RULES='## Harness rules — read first, apply always
- Output exactly ONE block of text per run. The harness posts your output as a single comment. STOP after producing it.
- Do NOT call `gh issue comment` via Bash — the harness handles posting. Doing so causes duplicate comments.
- If the last comment in the thread was posted by you (the agent) and ends with a question the user has not yet answered, output nothing and stop — do not answer your own question or proceed with assumed defaults.
- If you need to ask the user a clarifying question, output the question and stop. Do not also answer it in the same response.'

  ISSUE_CONTENT=$(gh issue view "$ISSUE_NUM" --repo "$REPO" \
    --json title,body,comments \
    --jq '"<!-- issue_number: '"$ISSUE_NUM"' -->\n# " + .title + "\n\n" + .body + (if (.comments | length) > 0 then "\n\n---\n\n## Thread so far\n\n" + ([.comments[] | "**" + .author.login + ":** " + .body] | join("\n\n---\n\n")) else "" end)')

  PROMPT="$HARNESS_RULES

$ISSUE_CONTENT"

  # Read model label and map to a Claude model ID.
  MODEL_LABEL=$(gh issue view "$ISSUE_NUM" --repo "$REPO" \
    --json labels \
    --jq '[.labels[].name] | map(select(startswith("model:"))) | first')

  case "$MODEL_LABEL" in
    "model:opus")  CLAUDE_MODEL="claude-opus-4-8" ;;
    "model:haiku") CLAUDE_MODEL="claude-haiku-4-5-20251001" ;;
    *)             CLAUDE_MODEL="claude-sonnet-4-6" ;;
  esac

  echo "[$(date '+%H:%M:%S')] Running issue #$ISSUE_NUM on $CLAUDE_MODEL"

  RESULT=$(cd "$REPO_DIR" && claude --model "$CLAUDE_MODEL" --print "$PROMPT" 2>&1)
  EXIT_CODE=$?

  if [ -n "$(echo "$RESULT" | tr -d '[:space:]')" ]; then
    gh issue comment "$ISSUE_NUM" --repo "$REPO" --body "$RESULT"
  fi

  if [ $EXIT_CODE -eq 0 ]; then
    gh issue edit "$ISSUE_NUM" --repo "$REPO" \
      --remove-label "agent:status:doing" \
      --add-label "agent:status:done,$MODEL_LABEL"

    # Auto-commit whatever the skill wrote — memory, learning progress,
    # journal entries — so a headless run leaves the repo in the same state
    # an interactive session would.
    CHANGED=$(git -C "$REPO_DIR" status --porcelain \
      personal-professional-profile/learning/progress/ \
      personal-professional-profile/learning/learning-plan.md \
      personal-professional-profile/learning/learning-index.md \
      personal-professional-profile/career/achievement-log.md \
      personal-professional-profile/interview-prep/story-bank/ \
      .claude/memory/ \
      journal/ 2>/dev/null)
    if [ -n "$CHANGED" ]; then
      git -C "$REPO_DIR" add \
        personal-professional-profile/learning/progress/ \
        personal-professional-profile/learning/learning-plan.md \
        personal-professional-profile/learning/learning-index.md \
        personal-professional-profile/career/achievement-log.md \
        personal-professional-profile/interview-prep/story-bank/ \
        .claude/memory/ \
        journal/ 2>/dev/null
      git -C "$REPO_DIR" commit -m "agent: update from issue #$ISSUE_NUM" 2>/dev/null
      git -C "$REPO_DIR" push origin main 2>/dev/null
      echo "[$(date '+%H:%M:%S')] Committed changes from issue #$ISSUE_NUM"
    fi

    echo "[$(date '+%H:%M:%S')] Done: issue #$ISSUE_NUM"
  else
    gh issue edit "$ISSUE_NUM" --repo "$REPO" \
      --remove-label "agent:status:doing" \
      --add-label "agent:status:failed"
    echo "[$(date '+%H:%M:%S')] Failed: issue #$ISSUE_NUM"
  fi
}

echo "Watcher running | Repo: $REPO | Machine: $MACHINE_LABEL"
echo "Polling every ${POLL_INTERVAL}s — Ctrl+C to stop"
echo ""

while true; do
  ISSUES=$(gh issue list \
    --repo "$REPO" \
    --label "agent:status:todo" \
    --label "$MACHINE_LABEL" \
    --json number \
    --jq '.[].number')

  for ISSUE_NUM in $ISSUES; do
    # Flip the label synchronously before backgrounding — prevents double
    # pickup if the next poll fires before the background process changes it.
    gh issue edit "$ISSUE_NUM" --repo "$REPO" \
      --remove-label "agent:status:todo" \
      --add-label "agent:status:doing" 2>/dev/null
    run_issue "$ISSUE_NUM" &
  done

  sleep $POLL_INTERVAL
done
