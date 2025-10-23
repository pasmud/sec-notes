# Access-control review guide

Use this guide when a role name alone cannot answer whether someone should be
able to perform an action. Start with the approved business rule, then compare
it to the effective policy and owner-provided test results. This synthetic Cedar
Desk example covers assigned-case read and single-case export in staging only.
It uses no live requests or real case records.

## Role and resource matrix

Here, Cedar and Birch are synthetic teams. A case is assigned to a team, not an
individual. `Allow` and `Deny` are intended outcomes, not test results.

| Operation | Case relationship | Cedar assistant | Cedar supervisor | Signed-in user with no case role |
| --- | --- | --- | --- | --- |
| Read case | Assigned to Cedar | Allow | Allow | Deny |
| Read case | Assigned to Birch | Deny | Deny | Deny |
| Export case | Assigned to Cedar | Deny | Allow | Deny |
| Export case | Assigned to Birch | Deny | Deny | Deny |

For another review, have the control owner approve each allow rule and define
how the service determines the resource relationship. Mark unlisted operations
such as bulk export out of scope; do not infer their behavior from this matrix.
If roles can combine or inherit privileges, add rows or columns for those
effective roles instead of assuming that role labels describe all permissions.

## Verify from approved artifacts

1. **Record the expected decision.** Reference the approved matrix revision and
   name the role, action, and resource relationship for each case under review.
2. **Compare effective policy.** Look for the matching environment and release,
   the effective grant after inheritance and overrides, and the team restriction
   at the server-side decision point. UI visibility does not establish a grant
   or denial. Record unclear inheritance or missing policy context as unverified.
3. **Review owner-run regression summaries.** For a single-case export review,
   compare Cedar supervisor/Cedar case (allow), Cedar assistant/Cedar case (deny),
   Cedar supervisor/Birch case (deny), and no case role/Cedar case (deny). Each
   result should identify the fixture, release, expected decision and observed
   decision, including whether a denied case produced any export output. The
   allowed case helps distinguish correct denials from an unavailable feature.
4. **Record the gap at the level the evidence supports.** In the
   [Cedar Desk report](../examples/cedar-report.md), `E-01` supports an assistant
   export grant discrepancy. It does not prove that an export was possible or
   that the team boundary failed. Record the policy gap and leave behavior
   unverified until the release-matched results are available.
