# Control review checklist

Use approved, revision-tagged material. For each item, record the expected control,
observed state, evidence ID, and one of: `supported`, `gap observed`, `not verified`,
or `not applicable` with justification. `Not verified` is not a pass. The sample
artifacts below are inputs for review, not instructions to exercise a live system.

## Authentication and access control

| Review question | Useful artifact or comparison |
| --- | --- |
| Are credential and sign-in requirements aligned with policy, especially for privileged roles? | Compare the approved policy with a sanitized identity policy export, including exception scope and expiry. |
| Do session duration, logout, and account revocation match the documented policy? | Review effective session settings and owner-run regression results for sign-out and deprovisioning in an isolated synthetic fixture. |
| Does the server enforce access decisions for each sensitive operation? | Compare the role/action matrix to policy definitions, reviewed code, and owner-run allow/deny regression results. A hidden UI control is not evidence of server-side enforcement. |
| Are record ownership and tenant boundaries included in access decisions? | Compare the data-access design to regression summaries that cover permitted same-tenant cases and denied synthetic cross-tenant cases. |
| Are privileged and service roles narrowly scoped and time-bounded where appropriate? | Review sanitized grants, approvals, and evidence of periodic access review or time-bound exception renewal. |
| Are access decisions auditable without disclosing secrets or personal data? | Review the audit schema and a sanitized synthetic record for the decision, actor category, and timestamp. |

## Deployment configuration

| Review question | Useful artifact or comparison |
| --- | --- |
| Does the effective configuration match the approved environment baseline? | Compare a revision-tagged effective configuration record with the baseline; distinguish defaults from overrides and name the environment. |
| Are diagnostic output and access to operational interfaces appropriately restricted? | Compare approved runtime settings and exposure inventory to the baseline, including explicit exceptions. |
| Do identity and secret-handling settings follow policy? | Review service role declarations and references to managed secrets; do not collect values. |
| Do transport and ingress configuration meet the approved design? | Compare the owner-provided listener and policy inventory with approved exposure and transport requirements. |
| Are release approvals, dependency maintenance, and rollback responsibilities clear? | Review release records, the dependency inventory and update policy, and documented recovery ownership. |
| Are audit, retention, and recovery controls configured for this environment? | Compare effective settings with policy and review a dated, owner-provided recovery exercise summary if authorized. |

If two artifacts disagree, record the discrepancy and ask the owner which revision
and source describe the effective control. An intended baseline or proposed change
alone does not demonstrate behavior. Use [triage and verification](triage-and-verification.md)
to decide what evidence would resolve the gap.
