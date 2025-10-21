"""Check the notebook index and a small subset of Markdown links offline."""

from __future__ import annotations

import argparse
import re
import stat
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath

INDEX = PurePosixPath("README.md")
SECTIONS = ("notes", "templates", "examples")
LINK = re.compile(r"(?<!!)\[[^\[\]]+\]\(([^()]*)\)")
INLINE_CODE = re.compile(r"(?<!`)`[^`]+`(?!`)")
FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
HEADING = re.compile(r"^ {0,3}#{1,6}[ \t]+(.+)$")
EXTERNAL = re.compile(r"^(?:https?://|mailto:)", re.IGNORECASE)
PATH_PART = re.compile(r"[A-Za-z0-9_.-]+")
ANCHOR = re.compile(r"[a-z0-9_-]+")


@dataclass
class Page:
    anchors: dict[str, int] = field(default_factory=dict)
    links: list[tuple[int, str]] = field(default_factory=list)


def parse_page(text: str) -> tuple[Page, list[tuple[int, str]]]:
    page = Page()
    problems: list[tuple[int, str]] = []
    opened: tuple[str, int] | None = None
    for number, line in enumerate(text.splitlines(), 1):
        marker = FENCE.match(line)
        if opened:
            fence, _ = opened
            if marker:
                run, rest = marker.groups()
                if run.startswith(fence) and not rest.strip():
                    opened = None
            continue
        if marker:
            run, rest = marker.groups()
            if run[0] == "~" or "`" not in rest:
                opened = (run, number)
                continue

        heading = HEADING.match(line)
        if heading and heading[1].isascii():
            plain = re.sub(r"[^a-z0-9_\s-]", "", heading[1].lower())
            slug = "-".join(plain.split())
            if slug in page.anchors:
                first = page.anchors[slug]
                problems.append((number, f"duplicate anchor #{slug} (first on line {first})"))
            elif slug:
                page.anchors[slug] = number

        prose = INLINE_CODE.sub(" ", line)
        page.links.extend((number, link[1]) for link in LINK.finditer(prose))

    if opened:
        problems.append((opened[1], "unclosed code fence"))
    return page, problems


def link_target(source: PurePosixPath, destination: str) -> tuple[PurePosixPath, str]:
    path, separator, fragment = destination.partition("#")
    if separator and not ANCHOR.fullmatch(fragment):
        raise ValueError("expected a nonempty heading fragment")
    if not path:
        if separator:
            return source, fragment
        raise ValueError("empty link destination")

    parts = path.split("/")
    parents = 0
    while parents < len(parts) and parts[parents] == "..":
        parents += 1
    if parents >= len(source.parts):
        raise ValueError("path leaves the notebook root")
    tail = parts[parents:]
    if not tail or any(p in (".", "..") or not PATH_PART.fullmatch(p) for p in tail):
        raise ValueError("expected a relative file path with optional leading ../")

    base = source.parts[: -(parents + 1)]
    return PurePosixPath(*base, *tail), fragment


def require_path(root: Path, relative: PurePosixPath, *, directory: bool = False) -> Path:
    """Inspect each component without following symlinks inside the root."""
    current = root
    for index, part in enumerate(relative.parts, 1):
        current /= part
        mode = current.lstat().st_mode
        if stat.S_ISLNK(mode):
            raise ValueError("symlinks are not supported")
        if directory or index < len(relative.parts):
            if not stat.S_ISDIR(mode):
                raise ValueError("expected a directory")
        elif not stat.S_ISREG(mode):
            raise ValueError("expected a regular file")
    return current


def check(root: Path) -> tuple[int, list[str]]:
    """Return the readable page count and deterministic diagnostics."""
    issues: list[str] = []
    try:
        root = root.resolve(strict=True)
        if not root.is_dir():
            return 0, ["root: expected a directory"]
    except (OSError, RuntimeError, ValueError):
        return 0, ["root: cannot resolve notebook directory"]

    candidates = [INDEX]
    for name in SECTIONS:
        section = PurePosixPath(name)
        try:
            directory = require_path(root, section, directory=True)
            entries = (section / entry.name for entry in directory.iterdir() if entry.suffix == ".md")
            candidates.extend(sorted(entries))
        except FileNotFoundError:
            continue
        except ValueError as error:
            issues.append(f"{section}: {error}")
        except OSError:
            issues.append(f"{section}: cannot list directory")

    pages: dict[PurePosixPath, Page] = {}
    for candidate in candidates:
        try:
            text = require_path(root, candidate).read_text(encoding="utf-8")
        except UnicodeDecodeError:
            issues.append(f"{candidate}: expected UTF-8 text")
        except ValueError as error:
            issues.append(f"{candidate}: {error}")
        except OSError:
            issues.append(f"{candidate}: cannot read notebook page")
        else:
            page, problems = parse_page(text)
            pages[candidate] = page
            issues.extend(f"{candidate}:{line}: {message}" for line, message in problems)

    edges: dict[PurePosixPath, set[PurePosixPath]] = defaultdict(set)
    for source, page in pages.items():
        for line, destination in page.links:
            if EXTERNAL.match(destination):
                continue
            try:
                target, fragment = link_target(source, destination)
                if target not in pages:
                    require_path(root, target)
                    if fragment:
                        raise ValueError("fragments require a readable notebook page")
                else:
                    if fragment and fragment not in pages[target].anchors:
                        raise ValueError(f"heading #{fragment} does not exist")
                    edges[source].add(target)
            except FileNotFoundError:
                issues.append(f"{source}:{line}: {destination!r}: target does not exist")
            except OSError:
                issues.append(f"{source}:{line}: {destination!r}: cannot inspect target")
            except ValueError as error:
                issues.append(f"{source}:{line}: {destination!r}: {error}")

    if INDEX in pages:
        reached = {INDEX}
        pending = [INDEX]
        while pending:
            unseen = edges[pending.pop()] - reached
            reached.update(unseen)
            pending.extend(unseen)
        for orphan in sorted(pages.keys() - reached):
            issues.append(f"{orphan}: not reachable from {INDEX}")
    return len(pages), issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path.cwd())
    args = parser.parse_args(argv)
    count, issues = check(args.root)
    if issues:
        for issue in issues:
            print(issue, file=sys.stderr)
        print(f"{len(issues)} issue(s) in {count} readable notebook page(s).", file=sys.stderr)
        return 1
    print(f"Checked {count} notebook page(s); no issues.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
