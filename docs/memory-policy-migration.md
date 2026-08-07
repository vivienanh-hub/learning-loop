# Migrating from the 3-Occurrence Rule

Earlier Learning Loop versions promoted any pattern seen in three sessions. That rule was easy to apply but mixed facts, events, inferences, and workflow defects into one threshold.

## What changes

| Before | Now |
|---|---|
| Three mentions could become a durable pattern | Behavioural inferences need three independent episodes, candidate status, learner confirmation, and expiry |
| Explicit goals waited for repetition | Explicit facts, goals, constraints, and preferences can persist immediately with provenance and review dates |
| A workflow failure needed recurrence | One reproduced, inspectable defect can justify a procedural correction |
| Evidence and tutoring rule could share one file | Evidence, inference, and intervention stay linked but distinct |
| Memories stayed active indefinitely | Confirmed memories have review or expiry rules and observed effects |
| Founding records were written freehand at setup | Founding records are admitted explicitly, carry the same metadata as everything else, and review at 90 days |

## Incremental migration

Do not rewrite every memory file at once.

1. Copy `docs/memory-policy.md` into your private workspace as `system/memory-policy.md`.
2. Create `journal/memory-effects.md` with the table from the policy.
3. Update the shipped commands so they refer to the policy.
4. When a legacy memory is next used or edited, add the fields from [the record template](../examples/memory-record-template.md).
5. Treat unsupported behavioural claims as candidates until confirmed.
6. Retire or correct contradicted memories; do not erase source episodes unless deletion is requested.
7. Use `/context-audit` to review the highest-impact memories first.
8. Bring the founding records up first — `user_profile.md` and the goal cascade. They were written before there was a policy to write them under, they are read by every tutor, and they are the cheapest records to migrate because you can confirm them from memory rather than from evidence.

## Migration priority

Review first any memory that:

- changes several tutors or workflows;
- contains sensitive or identity-like claims;
- has no inspectable source;
- contradicts recent behaviour;
- has been active for more than 90 days without confirmation;
- has produced an irrelevant, stale, or harmful effect.

The [synthetic memory audit](../examples/memory-audit-sample.md) shows what this looks like without exposing personal data.
