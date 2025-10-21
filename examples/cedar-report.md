# Cedar Desk review

**Fictional worked report.** Cedar Desk, its roles, release records, approval
references, and observations are invented. No systems were contacted.

## Summary and scope

Review `CD-17` covered case export policy for assistants and supervisors and
deployment artifacts for a fictional internal case-management application in
staging. The fictional service owner approved review of sanitized exports,
source diffs, and owner-provided regression summaries for October 14–17, 2025
(UTC). Production, real case records, direct environment interaction, and other
roles were excluded. Unexpected sensitive data or unclear scope would pause
review and be escalated through the approved channel to the designated data
custodian or scope owner, respectively. The fictional retention decision was
30 days with disposal by the review lead, subject to a hold.

One moderate finding remains open pending effective policy and regression
evidence. A second moderate finding was verified and closed for staging. No
conclusions were drawn about production.

## Evidence register

All entries below are synthetic, sanitized excerpts or summaries supplied by the
fictional service owner and reviewed by the fictional assessment lead.

| ID | Observed (UTC) | Source and scope | Minimum retained observation |
| --- | --- | --- | --- |
| E-01 | 2025-10-14 09:05 | Staging role matrix and effective policy, R24 | Matrix reserves case export for supervisors; effective policy lists export for assistants. |
| E-02 | 2025-10-14 09:25 | Staging baseline and effective settings, R24 | Baseline requires standard diagnostics; effective diagnostics are verbose. |
| E-03 | 2025-10-16 13:10 | Approved policy change, candidate R25 | Removes the assistant export grant and retains the supervisor grant. |
| E-04 | 2025-10-17 10:00 | Staging deployment record and effective settings, R25 | Deployment records R25; all three inventoried staging instances report standard diagnostics. |

## CD-01 — Assistant role includes export permission

**Observed:** The effective policy grants assistants a supervisor-only permission
(E-01). **Potential impact:** Excess privilege could make case information
available beyond business need if the export service honors that grant. The
review did not establish export behavior or real-data exposure. **Triage:**
Moderate, with high confidence in the policy discrepancy. Reviewed scope was
synthetic staging only; any evidence of matching production policy warrants an
authorized production scope decision and re-triage.

**Decision:** Identity owner to reconcile the grant and role matrix by October 24.
Close only when the deployed staging policy denies assistant export and an
owner-run regression summary for that release shows assistant denial and
supervisor allowance using synthetic records.

**Disposition (October 17): Open — needs evidence.** E-03 supports the proposed
policy change. E-04 identifies the staging release and diagnostics setting, but
does not establish the effective export policy or its behavior. The review lead
will follow up with the identity owner on October 24; reviewing new artifacts
requires renewed written authorization.

## CD-02 — Staging diagnostics exceed baseline

**Observed:** Staging ran verbose diagnostics against a standard-only baseline
(E-02). **Potential impact:** Extra operational detail could be retained in
central logs; log contents were not reviewed and disclosure was not observed.
**Triage:** Moderate, with high confidence in the configuration mismatch and
bounded exposure in the isolated staging environment.

**Decision:** Release owner to restore the baseline by October 17. Close when a
release record and effective-state snapshot identify the same release and all
inventoried staging instances show standard diagnostics.

**Disposition (October 17): Closed — verified.** The assessment lead matched
the release and all three staging instance settings in E-04 to the acceptance
criteria. The decision covers the current staging configuration only; historical
log contents and retention were not reviewed.
