---
description: Graded mock interview from a real job description
argument-hint: "[JD URL, #issue, or pasted JD]"
---

Mock job interview. Input is $ARGUMENTS — a JD URL, LinkedIn job URL, GitHub issue number (e.g. `#22`), or pasted JD text. Interview runs in chat; full transcript is posted to a GitHub issue at the end.

---

## Step 1 — Get the JD

**If $ARGUMENTS is a GitHub issue number** (e.g. `#22` or `22`):
- Run `gh issue view {number} --repo YOUR_GITHUB_USERNAME/YOUR_REPO` to get the issue body
- Extract the job listings. If the user specified a specific role, use that — otherwise ask.
- Extract the practice focus: use the **Custom focus** field if filled in, otherwise the **Practice focus** dropdown. Capture this as `{focus}` (or "none" if neither is set).
- Scan the issue body for attachment links — download each with an authenticated request and read it:
  ```
  curl -sL -H "Authorization: Bearer $(gh auth token)" "{attachment_url}" -o /tmp/{filename}
  ```
  If it specifies real interview structure — round names, focus areas, evaluation criteria — treat that as ground truth and use it in Steps 3 and 5.
- Rename the source issue:
  ```
  gh issue edit {issue_number} --repo YOUR_GITHUB_USERNAME/YOUR_REPO \
    --title "Interview Practice: {Company} — {Role Title}"
  ```

**If $ARGUMENTS is a LinkedIn URL containing `currentJobId=`:**
- Extract the ID and rewrite to `https://www.linkedin.com/jobs/view/{id}` before fetching.

**If $ARGUMENTS is any other URL:** fetch it directly.

**If $ARGUMENTS is pasted text:** use it directly.

Extract: company name, role title, seniority level, key requirements, must-have qualifications, any technical skills or domain knowledge called out.

Output the rename marker on its own line:

`<!-- title: Interview Practice: {Company} — {Role Title} -->`

---

## Step 2 — Read the CV

Read `cv/your_cv.tex` (or the CV file you've placed in `cv/`) silently. Note relevant experience, gaps, and strongest matches relative to the JD.

If no CV file exists at this path, ask the user where their CV is before continuing.

---

## Step 3 — Determine the interviewer persona

Infer who would realistically conduct this interview based on the role and company type:

- **Consulting firm:** Head of Delivery / VP of Products — pragmatic, delivery-focused, tests governance instincts and consulting mindset
- **Top-tier strategy firm:** Partner or Principal — highly structured, case-style follow-ups, expects sharp analytical reasoning
- **Startup / scale-up:** CPO or Head of Product — moves fast, cares about ownership, probes for bias toward action and shipping
- **Large tech / unicorn:** VP of Product — wants depth, probes for data-driven decisions and cross-functional leadership

State the persona clearly before starting: name, title, company, 1-sentence description of their interviewing style.

**If an attached document names the actual interviewer or round**, use that instead.

---

## Step 4 — Create a GitHub issue

Before the first question, create a GitHub issue to log this session:

```bash
INTERVIEW_URL=$(gh issue create \
  --repo YOUR_GITHUB_USERNAME/YOUR_REPO \
  --title "Interview Practice: {Company} — {Role Title} — {YYYY-MM-DD}" \
  --label "machine:yourname,agent:status:doing,model:{your running model}" \
  --body "$(cat <<'EOF'
## Interview Session

**Role:** {Role Title} at {Company}
**JD reference:** {URL or "pasted JD"}
**Date:** {today's date}
**Interviewer persona:** {inferred title and name}
**Practice focus:** {focus, or "None — balanced interview"}
**Status:** In Progress

---

*Transcript will be posted as a comment when the interview is complete.*
EOF
)")
INTERVIEW_NUM=$(echo "$INTERVIEW_URL" | grep -o '[0-9]*$')
```

Tell the user the issue number and URL.

---

## Step 5 — Run the interview

**Before Q1, tell the user plainly, out of character:** "Answer live, unaided, in this chat — no drafting or editing your answer somewhere else first. This only tells you something real if it reflects what you'd actually say under pressure, not a rehearsed answer read back."

**If an attached document specifies real focus areas or evaluation criteria**, build the question set from those instead of the generic blocks below.

Otherwise, structure the session to simulate ~1 hour across 7–8 questions:

| Block | # Qs | Focus |
|-------|------|-------|
| Warm-up | 1 | Brief background + why this role/company |
| Product thinking | 2 | Strategy, prioritisation, product sense — at least one scenario grounded in the company's actual domain |
| Behavioural | 2 | STAR-format — themes relevant to the JD (leadership, cross-functional conflict, failure, ambiguity) |
| Role-specific depth | 2 | Tailored to the JD |
| Wrap-up | 1 | "Do you have any questions for me?" — evaluate the quality of their questions |

**If `{focus}` is not "none":** shift weighting toward it — add 1 extra question in that area.

**Interviewer behaviour:**
- Stay in character throughout
- Use the persona's style
- If an answer is vague, follow up once before moving on
- Do not volunteer the correct answer during the question

**After each answer, break character briefly and give:**

```
---
🎯 **Interviewer's read:** [1–2 sentences — honest internal reaction, score X/5]

💬 **Coaching:**
- [what to add, cut, or reframe]
- [what the interviewer was actually listening for]
- [if score ≥ 4, name what worked so they can repeat it]

✏️ **How to answer this better:**
Draw on the CV you read in Step 2. Write a stronger version using the user's own experience — specific roles, metrics, situations from their background. Format it as a concrete example they could actually say.

- If a strong match exists in their CV: "Here's how you could have framed this using [specific experience]..." then write the improved answer.
- If the CV has a partial match: use it as the anchor, note what's missing, and suggest how to bridge the gap.
- If there is no good match: say so directly. Then ask "Do you have an example of [X] I don't know about yet?" or flag it as a story they need to build.

Keep the model answer concise — 4–6 sentences, STAR structure where relevant, written in first person.
---
```

Then move immediately to the next question (back in character).

**Scoring guide:**
- 5 — Exceptional: specific, structured, memorable. Would move to offer.
- 4 — Strong: clear and credible, minor gaps. Would advance.
- 3 — Adequate: answered the question but lacked depth or specificity. Borderline.
- 2 — Weak: vague, generic, or missed what was being tested. Would not advance without improvement.
- 1 — Miss: off-topic, confused, or no real answer given.

**Hard cap:** for any diagnostic, prioritization, or roadmap-scenario question, a category-only answer — names the right problem area but never states a specific metric, threshold, or concrete next step — caps at 3, regardless of fluency. Reserve 4–5 for answers that close with a checkable mechanism: a number, a named signal, or a specific branch-by-outcome plan.

---

## Step 6 — Debrief and post transcript

After the final question, step fully out of character:

```
## Overall Debrief

**Interviewer impression:** [1–2 sentences as the hiring manager — would they move you forward?]
**Average score:** [X.X / 5]
**Strongest moment:** [which question + why it worked]
**Biggest gap to close:** [the single most important thing to fix before the real interview]
**Recommended practice:** [2–3 specific actions]
```

Then post the full transcript to the GitHub issue as a comment:

```bash
gh issue comment {issue_number} --repo YOUR_GITHUB_USERNAME/YOUR_REPO --body "$(cat <<'EOF'
## Interview Transcript — {YYYY-MM-DD}

**Q1 — [topic label]**
> [question text]

**A:**
[user's answer verbatim or close paraphrase]

**Feedback:** {score}/5 — [1-sentence summary]

---

[repeat for each question]

---

## Debrief

**Overall impression:** [sentence]
**Average score:** X.X / 5
**Strongest moment:** [Q# — why]
**Biggest gap:** [what to fix]
**Recommended practice:**
- [action 1]
- [action 2]
- [action 3]
EOF
)"
```

Then close the loop:

```bash
gh issue edit {issue_number} --repo YOUR_GITHUB_USERNAME/YOUR_REPO --remove-label "agent:status:doing" --add-label "agent:status:done"
```

Give the user the final issue URL and one sentence on what to work on before the real thing.

If the average score is 4.0+ or any single answer scored 5/5: *"Strong enough to bank — run `/portfolio-capture` before this just becomes a memory."*

---

**Write session log:**

Write `journal/sessions/{YYYY-MM-DD}-{HHMM}.md`:

```markdown
# Session: YYYY-MM-DD HH:MM — Interview Practice: {Company} — {Role Title}

## What we covered
- Mock interview: {Role Title} at {Company}
- Interviewer persona: {name and title}
- {N} questions — {blocks covered}
- Average score: {X.X} / 5

## What clicked / was decided
- [strongest answers and what worked]
- [key coaching points that landed]

## Evidence worth saving
- [answers scored 4–5/5 — bank these for story use]

## Open threads
- [gaps to close before the real interview]
- [stories to build]
```

---

## Token usage estimate

`_Complexity: ~X input / ~Y output tokens (est.)_`
