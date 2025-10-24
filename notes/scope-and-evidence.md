# Scope and evidence

## Authorization gate

Before opening review artifacts, use the [authorization worksheet](../templates/authorization.md)
to record an accountable approver, named reviewers, a time window with timezone,
approved systems or components, and the exact artifact sets and review methods.
Confirm the evidence classification, permitted recipients and storage, and who
can authorize a restart. A ticket number, access to a folder, or verbal consent
alone does not establish permission. Record where the signed approval is held.

Review only the approved artifacts: for example, a sanitized policy export for
one named environment or a code snapshot at a specified revision. Treat ambiguity
as out of scope. A reference from an approved artifact to a different environment
does not extend permission; record the dependency as a coverage gap and request
a scope amendment if needed.

## Stop and escalation

| Trigger | Immediate action | Condition to resume |
| --- | --- | --- |
| Scope is unclear, expired, or the artifact appears to be from another environment | Stop review of the affected item; record a safe reference and notify the scope owner | Current written authorization explicitly covers it |
| A secret, personal data, or restricted record appears unexpectedly | Stop viewing or copying it; notify the designated incident or privacy contact through the approved channel | The handling owner approves a sanitized replacement and restart |
| There is suspected active harm or an operational impact | Halt assessment activity and hand off through the incident process; leave preservation and containment to that process | The incident lead and scope owner authorize resumption |
| Approved storage or recipient controls are unavailable | Stop collecting or sharing evidence | The approved handling path is restored or replaced in writing |

Record the time, broad trigger, who was notified, and state (`paused`, `resumed`,
or `closed`) without repeating sensitive material. Do not delete or alter material
subject to an incident hold; follow the designated custodian's instructions.

## Evidence handling

1. **Define the claim first.** Ask what is the smallest artifact that establishes
   the observation. A setting name and its effective state may be enough; an
   entire configuration export is usually unnecessary.
2. **Record provenance.** Give the evidence a stable ID. Record the source type,
   environment, revision or release, and observation time in UTC. Distinguish an
   owner-provided artifact from one independently reviewed by the assessor.
3. **Minimize and redact.** Prefer a newly written plain-text excerpt. Omit
   unrelated fields and replace sensitive values with a label such as
   `[REDACTED: account identifier]`. Preserve distinctions needed for the claim
   (for example, `Role A` versus `Role B`). Do not rely on hidden text, overlays,
   or cropping to remove underlying data from shareable documents.
4. **Review the shareable copy.** Reopen the exported file; inspect visible text,
   metadata, and attachments when applicable. Check that the excerpt still supports
   the claim and that names, paths, timestamps, and IDs do not disclose more than
   approved. Have an authorized second reviewer check sensitive excerpts before
   sharing, according to local procedures.
5. **Control access and retention.** Use the approved restricted store and share
   sanitized excerpts only with approved recipients. Record the disposal owner,
   deadline, and any hold. A report index can refer to an evidence ID without
   disclosing the original storage path.

**Synthetic example:** `E-04 | sanitized policy snapshot | staging | fixture R8 |
2025-10-14 09:30 UTC | Support role: export permission enabled`. The observation
does not require a real account ID, exported record, or full role membership list.

The [worked redaction and retention example](../examples/cedar-evidence-handling.md)
shows how to keep the evidence needed for a configuration claim while removing
instance identifiers and documenting who will dispose of each review copy.
