---
description: Match your profile against a target role — gaps and pitch angle
argument-hint: "[JD URL or pasted JD]"
---

Match a job description against your CV and return targeted recommendations. Input is $ARGUMENTS — a job URL or pasted job description.

---

## Model gate (when an issue number is provided — run this first, before anything else)

If the prompt contains `<!-- issue_number: N -->`, read the issue's model label and enforce it:

```bash
gh issue view N --repo YOUR_GITHUB_USERNAME/YOUR_REPO --json labels -q '[.labels[].name] | map(select(startswith("model:"))) | first'
```

If the label does **not** match your current model, output this and **stop — do not continue**:
> ⚠️ This issue is labeled `{label}` but you're on `{your model}`. Switch first: `/model {correct-model-id}`, then re-run.

---

## Step 1 — Get the job posting

If $ARGUMENTS is a LinkedIn URL containing `currentJobId=`, extract the ID and rewrite to `https://www.linkedin.com/jobs/view/{id}` before fetching.

If $ARGUMENTS is any other URL, fetch it directly.

If $ARGUMENTS is pasted text, use it directly.

Extract: company name, role title, key requirements, and seniority level.

---

## Step 2 — Read the CV

Read `cv/your_cv.tex` (or the CV file you've placed in `cv/`) silently.

If no CV file exists, read `personal-professional-profile/career/experience.yaml` and `personal-professional-profile/career/cv-bullet-bank.md` as a substitute.

---

## Step 3 — Output the rename marker

Before writing anything else, output this line:

`<!-- title: [CV Match] {Company} — {Role Title} -->`

If the prompt contains `<!-- issue_number: N -->`, rename the issue immediately:
```bash
# Use the label for the model you are actually running — model:sonnet, model:opus,
# or model:haiku. Never hardcode one: the model gate above compares this label
# against your running model, so a wrong value fails the gate on the next run.
gh issue edit N --repo YOUR_GITHUB_USERNAME/YOUR_REPO --title "[CV Match] {Company} — {Role Title}" --add-label "model:{your running model}"
```

---

## Step 4 — Write the analysis

Produce a structured CV match analysis covering:

- **Overall verdict** — match strength in one sentence, with the core reason
- **What maps well** — a table mapping your experience to role requirements
- **Gaps to address** — specific gaps, numbered, with explanation of why each matters
- **What to do before applying** — concrete rewrites or additions to the CV, named by bullet/section
- **One-line pitch angle** — a ready-to-use framing for the cover note or opening summary

Be direct. Flag salary risk if the role appears below your stated salary target.

If the match surfaces a genuinely strong angle that isn't already captured anywhere — a piece of evidence or framing put into words for the first time — name it and add: *"That's positioning material, not just analysis — worth `/portfolio-capture` or a line in `cv-bullet-bank.md` before it's lost."*

---

## Token usage estimate

`_Complexity: ~X input / ~Y output tokens (est.)_`
