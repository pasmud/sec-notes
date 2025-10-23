# sec-notes

An offline notebook for reviewing security controls using approved design,
configuration, and test artifacts. It takes a reviewer from written scope to a
short report that distinguishes what was observed, what was inferred, and what
still needs verification.

## Quickstart

1. Start with [scope and evidence](notes/scope-and-evidence.md). Copy the
   [authorization worksheet](templates/authorization.md) into an approved work
   location and get written approval before reviewing artifacts.
2. Use the [control review checklist](notes/control-review.md) to record both
   what you reviewed and what you could not establish. For role and ownership
   boundaries, use the [access-control review guide](notes/access-control-review.md).
   Record only approved, minimized evidence references in the [finding template](templates/finding.md).
3. Use [triage and verification](notes/triage-and-verification.md) to agree on
   priority, ownership, and closure criteria. The [worked report](examples/cedar-report.md)
   shows a deployment finding that closes and an access-control finding that
   stays open after a proposed change.

For a dry run, read the worked report and compare its disposition for each
finding against the closure criteria. For real reviews, keep completed worksheets
and evidence in your organization's approved storage, not in this repository.

## Offline documentation checks

From the repository root, with Python 3.10 or newer and no third-party packages:

```sh
python3 tools/check_notes.py
python3 -m unittest discover -s tests -v
python3 -m tabnanny tools tests
git diff --check
```

The checker reads `README.md` and the direct `*.md` files in `notes/`,
`templates/`, and `examples/`. These pages must be reachable from the README
through local links, directly or via another notebook page. An optional root
argument lets you run the same checks against another local notebook tree.

- Use inline links such as `[Checklist](notes/control-review.md)` and
  `[Evidence](notes/scope-and-evidence.md#evidence-handling)`. Paths are relative
  to the source page, case-sensitive on case-sensitive filesystems, with no URL
  escaping, query strings, or literal spaces. Use ASCII letters, digits, dots,
  underscores, and hyphens in path components. Leading `../` segments are allowed
  within the notebook root. Targets must be regular files, reached without symlinks.
- Fragments are supported for notebook Markdown pages only. Use plain ASCII ATX
  headings: for example, `## Evidence handling` gives `#evidence-handling`.
  The checker lowercases headings, replaces runs of whitespace with hyphens,
  and drops punctuation other than hyphens and underscores. Duplicate generated
  anchors are reported; duplicate headings are not auto-numbered.
- The checker skips fenced code, simple inline code spans, images, and
  `http`, `https`, and `mailto` destinations. It does not validate external
  URLs or implement a general Markdown parser (reference links, indented code,
  raw HTML, and nested link syntax are outside its contract).
- Exit status `0` means no issues, `1` means notebook issues were reported, and
  `2` means invalid command-line usage. Diagnostics identify the file and line
  when available.

The checker is intended for small local notebook trees that are not changing
during a check. It does not assess systems or certify that an assessment is
complete. The notebook does not substitute for written authorization, incident
procedures, or production assurance. All examples and test fixtures are synthetic.

## License and timeline

[MIT](LICENSE). The October 2025 commit timeline is illustrative and is not
evidence of activity on those dates.
