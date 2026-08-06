---
name: memory-record-slug
description: "One-line summary specific enough to decide relevance"
metadata:
  type: user | feedback | project | reference
  memory_type: semantic | procedural
  claim_type: explicit | inference | defect | intervention
  status: candidate | confirmed | disputed | retired
  sensitivity: low | medium | high
  created: YYYY-MM-DD
  last_confirmed: YYYY-MM-DD | null
  review_by: YYYY-MM-DD | null
  expires: YYYY-MM-DD | null
  sources:
    - journal/sessions/YYYY-MM-DD-HHMM.md
  consumers:
    - mentor
---

# Memory statement

[State the fact, inference, defect, or intervention. Do not rewrite a model inference as the learner's own words.]

## Evidence

- [Distinct event or explicit statement, with a source link]

## Behaviour changed

[Describe exactly how this record may change guidance or workflow behaviour. Candidates, disputed records, retired records, and expired records change nothing.]

## Review and falsification

- Confirm when: [evidence or learner action]
- Revisit when: [date, contradiction, or event]
- Retire when: [condition]
- Delete when: [condition or learner request]

## Effect history

Material uses are recorded in `journal/memory-effects.md` as `helpful`, `irrelevant`, `stale`, or `harmful`.
