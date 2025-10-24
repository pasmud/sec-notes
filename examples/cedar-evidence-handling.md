# Cedar Desk evidence handling example

All fields, identifiers, and handling decisions below are synthetic. This is
the effective-settings portion of `E-04` in the
[Cedar Desk report](cedar-report.md#evidence-register). The claim is that all
three inventoried staging instances on `R25` showed standard diagnostics at
the time of the snapshot. The separate deployment record ties `R25` to staging.

## Before and after redaction

**Before — approved source excerpt in the restricted review store:**

```text
Environment: staging
Release: R25
Observed: 2025-10-17 10:00 UTC
Inventory size: 3
fixture-cedar-07 | diagnostics=standard | contact=owner-a@example.invalid
fixture-cedar-08 | diagnostics=standard | contact=owner-a@example.invalid
fixture-cedar-09 | diagnostics=standard | contact=owner-b@example.invalid
```

**After — newly written excerpt for approved report recipients:**

```text
E-04 | owner-provided effective-settings snapshot
Environment: staging | Release: R25 | Observed: 2025-10-17 10:00 UTC
Inventory size: 3
Instance A | diagnostics=standard
Instance B | diagnostics=standard
Instance C | diagnostics=standard
```

The reviewer replaced instance IDs with distinct labels and omitted contact
addresses. The second reviewer compared the rows one-to-one in restricted
storage, then reopened the plain-text excerpt to confirm it retained three
distinct rows, the release, and the observation time without the original
identifiers. No identity mapping is needed in the report. The excerpt does
not establish past diagnostics settings, log contents, or production behavior.

## Retention record

The fictional `CD-17` approval gives review copies 30 days from collection.
For `E-04`, collected at 10:00 UTC on October 17, the deadline is **November
16, 2025 at 10:00 UTC**. The review lead owns disposal.

| Copy | Approved location and access | At the deadline, if no hold applies |
| --- | --- | --- |
| Review copy of the snapshot | Restricted evidence store; named reviewers only | Review lead removes it using the store's approved disposal process. |
| Sanitized excerpt in the report | Approved report store; reviewers and designated report recipients | Review lead removes the excerpt and coordinates disposal of any approved distributed copies. |

Before disposal, the lead checks with the designated custodian for holds. If
held, the lead preserves the affected copies in restricted storage and records
the hold owner and next review date. Otherwise, the lead records `E-04`, the
copy types, completion time and any outstanding copies in the handling log
without copying evidence into it. The source system's records are outside
this review-copy schedule.
