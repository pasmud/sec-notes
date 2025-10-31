# Harbor cloud configuration case study

**Scope:** Fictional approval `HB-03` covers the configuration of the cloud
control-plane audit route and its named destination in the Harbor sandbox
project. The review uses only offline, owner-provided synthetic artifacts.
Log contents, organization-level archives, and other projects are out of scope.

## Evidence trail

| ID | Reviewed (UTC) | Artifact | Observation |
| --- | --- | --- | --- |
| HB-E01 | 2025-10-30 09:00 | Approved sandbox baseline `B4` and exception register | Control-plane audit events must be routed to the designated `Sandbox Audit` store, which must retain them for at least 30 days. No active exception covers that store. |
| HB-E02 | 2025-10-30 09:05 | Effective route snapshot `S12`, collected at 08:30 UTC | The route is enabled for control-plane audit events and names `Sandbox Audit` as its destination. |
| HB-E03 | 2025-10-30 09:10 | Effective lifecycle snapshot `S12`, collected at 08:30 UTC | The same project's `Sandbox Audit` store expires objects after seven days. |
| HB-E04 | 2025-10-30 09:20 | Approved infrastructure change `C13` | The proposed setting is 30 days; no apply record or later effective snapshot was supplied. |

## Findings and follow-up

- **Routing configuration supported:** `HB-E02` matches the destination and
  event category in `HB-E01`. This establishes the configured route only;
  delivery and event completeness were not verified.
- **Retention gap observed:** `HB-E03` is direct evidence that the named store
  fell short of `HB-E01` at 08:30 UTC. `HB-E04` changes the intended setting
  but does not establish that it took effect. The shorter setting could limit
  retrospective review at this store. The artifacts do not show that events
  were lost or that no organization-level archive exists.
- **Disposition: open — needs evidence.** The cloud platform owner will supply
  an apply record for `C13` and a newer effective snapshot of the same store
  showing at least 30 days, including any applicable lifecycle overrides. The
  review lead will revisit the configuration finding on November 4. Closure
  would cover that store's configuration only, not historical log availability.
