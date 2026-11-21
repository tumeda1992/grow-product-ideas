#!/usr/bin/env python3
"""Check local references in a product plan without changing files or fetching URLs."""
import argparse
import html
import json
import re
import sys
import unicodedata
from pathlib import Path
from urllib.parse import unquote, urlsplit


def prose(text):
    fence = None
    comment = False
    for number, line in enumerate(text.splitlines(), 1):
        # Block quotes are containers: definitions and fences inside them are
        # Markdown too. Preserve source line numbers after removing containers.
        original_line = line
        quote_depth = 0
        quote_ends = []
        while True:
            quote = re.match(r"^ {0,3}>[ \t]?", line)
            if quote is None:
                break
            quote_depth += 1
            line = line[quote.end():]
            quote_ends.append(len(original_line) - len(line))
        # A quoted fence ends when its containing quote ends, even without an
        # explicit closing marker. A nested quote may end while its parent stays.
        if fence and quote_depth < fence[2]:
            fence = None
        if fence:
            # Extra quote markers inside code are literal, not containers.
            line = original_line[quote_ends[fence[2] - 1]:] if fence[2] else original_line
        match = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
        if match:
            marker, tail = match.groups()
            if fence is None:
                fence = (marker[0], len(marker), quote_depth)
            elif marker[0] == fence[0] and len(marker) >= fence[1] and not tail.strip():
                fence = None
            continue
        if fence:
            continue
        parts = []
        while line:
            if comment:
                before, found, line = line.partition("-->")
                if not found:
                    break
                comment = False
            else:
                before, found, line = line.partition("<!--")
                parts.append(before)
                if not found:
                    break
                comment = True
        yield number, "".join(parts)
    if fence or comment:
        raise ValueError("unclosed fence or comment")


def anchors(text):
    found = set()
    counts = {}
    for _, line in prose(text):
        found.update(re.findall(r'<a\s+[^>]*id=["\']([^"\']+)["\']', line))
        match = re.match(r"^ {0,3}#{1,6}\s+(.+?)(?:\s+#+\s*)?$", line)
        if not match:
            continue
        title = html.unescape(re.sub(r"<[^>]*>", "", match[1])).strip().lower()
        slug = "".join(c for c in title if c in "-_ " or unicodedata.category(c)[0] in "LNM")
        slug = slug.replace(" ", "-")
        count = counts.get(slug, 0)
        counts[slug] = count + 1
        found.add(slug + (f"-{count}" if count else ""))
    return found


def destination(raw):
    match = re.fullmatch(r'''(?:<([^<>]+)>|([^\s<>]+))(?:\s+["'][^\n]*["'])?''', raw.strip())
    return html.unescape(match[1] or match[2]) if match else None


def inspect(root, selected=()):
    issues = []
    links = 0
    external = 0
    cache = {}
    files = [Path(p).resolve() for p in selected] if selected else sorted(root.rglob("*.md"))

    def issue(file, line, target, kind):
        issues.append({"file": str(file), "line": line, "target": target, "kind": kind})

    def check(file, number, target):
        nonlocal links, external
        try:
            url = urlsplit(target)
        except ValueError:
            issue(file, number, target, "invalid-target")
            return
        if url.scheme:
            if url.scheme.lower() in ("http", "https", "mailto"):
                external += 1
            else:
                issue(file, number, target, "unsupported-uri")
            return
        links += 1
        if target.startswith("/") or url.netloc or url.query:
            issue(file, number, target, "non-relative-or-unsupported-target")
            return
        path = (file.parent / unquote(url.path)).resolve() if url.path else file.resolve()
        if not path.is_relative_to(root):
            issue(file, number, target, "outside-plan")
        elif not path.exists():
            issue(file, number, target, "missing-target")
        elif url.fragment:
            if not path.is_file() or path.suffix.lower() != ".md":
                issue(file, number, target, "unverified-anchor-format")
                return
            if path not in cache:
                try:
                    cache[path] = anchors(path.read_text(encoding="utf-8"))
                except (OSError, UnicodeError, ValueError):
                    issue(file, number, target, "unverified-target-format")
                    return
            if unquote(url.fragment) not in cache[path]:
                issue(file, number, target, "missing-anchor")

    if not files:
        issue(root, 0, "", "no-markdown-files")
    for file in files:
        file = file.resolve()
        if not file.is_relative_to(root) or not file.is_file():
            issue(file, 0, "", "invalid-source")
            continue
        try:
            lines = list(prose(file.read_text(encoding="utf-8")))
        except (OSError, UnicodeError, ValueError):
            issue(file, 0, "", "unverified-source-format")
            continue
        definitions = {}
        body = []
        for number, line in lines:
            match = re.match(r"^ {0,3}\[([^\]]+)\]:\s*(.+)$", line)
            if match:
                target = destination(match[2])
                if target is None:
                    issue(file, number, match[2], "unverified-link-format")
                else:
                    definitions[match[1].strip().casefold()] = target
                    check(file, number, target)
            else:
                body.append((number, re.sub(r"(`+)(?!`).*?\1(?!`)", "", line)))
        for number, line in body:
            if re.search(r"<(?:a\b[^>]*href|img\b[^>]*src)\s*=", line, re.I):
                issue(file, number, "HTML reference", "unverified-link-format")
            # Deliberately bounded syntax: encode parentheses in paths as %28/%29.
            pattern = r"!?\[[^\[\]\n]*\]\(([^()\n]*)\)"
            for match in re.finditer(pattern, line):
                target = destination(match[1])
                if target is None:
                    issue(file, number, match[1], "unverified-link-format")
                else:
                    check(file, number, target)
            rest = re.sub(pattern, "", line)
            if "](" in rest:
                issue(file, number, rest, "unverified-link-format")
            for match in re.finditer(r"\[([^\[\]]+)\]\[([^\[\]]*)\]", rest):
                key = (match[2] or match[1]).strip().casefold()
                if key not in definitions:
                    issue(file, number, key, "missing-reference-definition")
            # Shortcut references resolve through a definition, already checked above.
    return {"ok": not issues, "files": len(files), "local_links": links,
            "external_not_fetched": external, "issues": issues}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", type=Path, help="Existing product plan directory")
    parser.add_argument("--file", action="append", default=[], help="Saved file; repeat for a handoff block")
    args = parser.parse_args()
    root = args.plan.resolve()
    if not root.is_dir():
        parser.error("plan must be an existing directory")
    result = inspect(root, args.file)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 2


if __name__ == "__main__":
    sys.exit(main())
