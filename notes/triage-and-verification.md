# Triage and verification

## Set priority with the owner

State the expected control and the observed deviation before describing its
potential impact. Name the affected environment, data or process, and known
exposure constraints. Label confidence independently: `high` for direct,
revision-matched evidence of the claim; `medium` for evidence that leaves relevant
conditions uncertain; `low` for indirect or conflicting evidence. A high-confidence
configuration observation can still have an uncertain impact.

| Priority | Decision rule | Handling |
| --- | --- | --- |
| Urgent | Credible indication of current severe harm or imminent material exposure | Notify the designated response contact immediately; follow stop rules |
| High | Plausible material impact and credible exposure under normal conditions | Assign an accountable owner and expedited target date |
| Moderate | Meaningful gap with bounded impact or demonstrated exposure constraints | Schedule a fix and review any assumptions at the next agreed checkpoint |
| Low | Limited impact, including isolated hygiene or documentation drift | Track in the owning team's normal maintenance backlog |

Record the rationale, owner, next decision date, and what could change the
priority. Unknown exposure is not evidence that exposure is low. Where confidence
is too low for a firm rating, record a provisional rating and a specific artifact
needed to resolve it. Keep accountable risk acceptance separate from remediation:
name the approver, rationale, review or expiry date, and residual risk.

## Close using positive evidence

1. Agree on acceptance criteria before the change: control, expected behavior,
   environment, required revision, and who reviews the evidence.
2. Use approved artifacts: reviewed changes, owner-run regression summaries from
   isolated synthetic fixtures, and effective-state snapshots or release records
   for the environment in scope. For access decisions, require both a permitted
   business case and denied cases that match the policy boundaries.
3. Confirm the evidence is scoped and current. A source diff can establish that
   a fix was proposed; it cannot establish deployment or effective behavior.
4. Record the disposition as `closed — verified`, `open — needs evidence`, or
   `risk accepted` with the approval record. Note residual risks and gaps in
   coverage even when closing. Reopen if a later artifact contradicts the closure
   evidence or the affected control regresses.

See the [worked report](../examples/cedar-report.md) for a closure decision based
on an effective-state record and for a finding that remains open.
