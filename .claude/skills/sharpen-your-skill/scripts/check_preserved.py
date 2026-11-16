#!/usr/bin/env python3
"""Report what an original skill contains that its sharpened version lost.

Usage:
    check_preserved.py <original skill dir or file> <sharpened skill dir or file>

Checked items: every non-empty line inside a fenced code block, every inline
code span, every URL, every bundled file, and every frontmatter key other than
`description`. An item counts as present when its text appears anywhere in the
sharpened skill's text files, ignoring differences in whitespace.

Exit 0: nothing missing (prints a line that starts with OK).
Exit 1: items missing (prints MISSING and one item per line).
Exit 2: bad arguments.
"""
import re
import sys
from pathlib import Path

TEXT_SUFFIXES = {".md", ".txt"}
FENCE = re.compile(r"^\s*(```|~~~)")
INLINE = re.compile(r"`([^`\n]+)`")
URL = re.compile(r"https?://[^\s)>\]\"'`]+")
KEY = re.compile(r"^([A-Za-z0-9_-]+):(.*)$")


def text_files(path: Path):
    if path.is_file():
        return [path]
    return sorted(
        f for f in path.rglob("*") if f.is_file() and f.suffix.lower() in TEXT_SUFFIXES
    )


def read_all(path: Path) -> str:
    return "\n".join(
        f.read_text(encoding="utf-8", errors="replace") for f in text_files(path)
    )


def squash(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def skill_md(path: Path):
    if path.is_file():
        return path
    candidate = path / "SKILL.md"
    return candidate if candidate.is_file() else None


def split_frontmatter(text: str):
    """Return (frontmatter lines, body). Frontmatter is empty when absent."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return [], text
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return lines[1:i], "\n".join(lines[i + 1 :])
    return [], text


def top_level_keys(frontmatter_lines):
    keys = {}
    for line in frontmatter_lines:
        if line[:1] in (" ", "\t", "#", "-"):
            continue
        match = KEY.match(line)
        if match:
            keys[match.group(1)] = match.group(2).strip()
    return keys


def payload_items(text: str):
    """Return an ordered list of (kind, value) found in markdown text."""
    found = []
    seen = set()

    def add(kind, value):
        value = value.strip()
        if value and (kind, value) not in seen:
            seen.add((kind, value))
            found.append((kind, value))

    in_fence = False
    prose = []
    for line in text.splitlines():
        if FENCE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            add("code line", line)
        else:
            prose.append(line)
    for match in INLINE.finditer("\n".join(prose)):
        add("inline code", match.group(1))
    for match in URL.finditer(text):
        add("url", match.group(0).rstrip(".,;:"))
    return found


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    old, new = Path(sys.argv[1]), Path(sys.argv[2])
    for path in (old, new):
        if not path.exists():
            print(f"Not found: {path}")
            return 2

    missing = []

    # Payload: code, inline code, URLs. Frontmatter is compared separately.
    old_body_parts = []
    for f in text_files(old):
        _, body = split_frontmatter(f.read_text(encoding="utf-8", errors="replace"))
        old_body_parts.append(body)
    items = payload_items("\n".join(old_body_parts))
    new_text = squash(read_all(new))
    for kind, value in items:
        if squash(value) not in new_text:
            missing.append((kind, value))

    # Bundled files: every file in the original must still exist.
    file_count = 0
    if old.is_dir() and new.is_dir():
        for f in sorted(p for p in old.rglob("*") if p.is_file()):
            relative = f.relative_to(old)
            file_count += 1
            if not (new / relative).is_file():
                missing.append(("file", str(relative)))

    # Frontmatter: same keys, same values, except description.
    key_count = 0
    old_md, new_md = skill_md(old), skill_md(new)
    if old_md and new_md:
        old_keys = top_level_keys(
            split_frontmatter(old_md.read_text(encoding="utf-8", errors="replace"))[0]
        )
        new_keys = top_level_keys(
            split_frontmatter(new_md.read_text(encoding="utf-8", errors="replace"))[0]
        )
        for key, value in old_keys.items():
            if key == "description":
                continue
            key_count += 1
            if key not in new_keys:
                missing.append(("frontmatter key", key))
            elif new_keys[key] != value:
                missing.append(
                    ("frontmatter value", f"{key}: was `{value}`, now `{new_keys[key]}`")
                )

    total = len(items) + file_count + key_count
    if missing:
        print(f"MISSING ({len(missing)} of {total} items checked):")
        for kind, value in missing:
            print(f"  [{kind}] {value}")
        return 1
    print(f"OK: all {total} items from the original are present.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
