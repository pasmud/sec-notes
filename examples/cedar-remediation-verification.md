# Cedar Desk remediation verification example

This fictional follow-up uses the
[remediation verification worksheet](../templates/remediation-verification.md)
for the open finding in the [Cedar Desk report](cedar-report.md).

- **Finding ID and expected control:** `CD-01`; supervisors may export a case
  assigned to their team; assistants may not export.
- **Original observation and evidence IDs:** `E-01` recorded an assistant export
  grant in staging `R24`; `E-03` documented the proposed removal.
- **Authorized environment, resource scope, and approval reference:** Staging
  single-case export only, synthetic records, follow-up approval `CD-17-F1`.
- **Remediation owner, verifier, and decision date (UTC):** Identity owner;
  assessment lead; October 24, 2025.
- **Change reference and deployed revision to verify:** `E-03`; staging `R25`,
  identified at deployment in `E-04` and in the follow-up policy snapshot `E-05`.

## Acceptance criteria

| Criterion and expected outcome | Required evidence | Evidence ID, scope, and observation | Result |
| --- | --- | --- | --- |
| Effective policy: no assistant export grant; supervisor grant limited to cases assigned to their team. | Release-matched effective policy snapshot. | `E-05`, owner-provided staging `R25` snapshot, October 24 09:00 UTC: assistant grant absent after inheritance; supervisor grant scoped to assigned-team cases. | Met |
| Assistant export of a synthetic case assigned to their team is denied and yields no export. | Owner-run regression summary for staging `R25` using isolated synthetic fixtures. | `E-06`, owner-provided summary, October 24 10:00 UTC: denial and no output on isolated candidate `R25-rc1`; no result for deployed revision `R25`. | Not verified |
| Supervisor export of a synthetic case assigned to their team succeeds. | Same release-matched summary. | `E-06`: expected output on `R25-rc1` only. | Not verified |

## Decision record

- **Disposition:** `open — needs evidence`.
- **Rationale:** The current policy matches expectations, but the candidate
  test results do not verify runtime decisions for the deployed revision.
- **Residual risk and coverage limits:** Runtime enforcement of assistant denial
  and supervisor allowance for `R25` is unverified. This worksheet does not
  verify other roles, cross-team runtime enforcement, or production.
- **Next action, accountable owner, and due date:** Identity owner supplies
  the two `R25` results by October 30, 2025; assessment lead confirms written
  authorization covers the new artifacts before review.
- **Reopen trigger:** Not applicable; the finding has not closed.
