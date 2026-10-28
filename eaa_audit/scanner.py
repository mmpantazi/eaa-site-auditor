"""Walk a built site folder, resolve its CSS, run every check."""

import os
from dataclasses import dataclass, field
from urllib.parse import unquote, urlparse

from .advice import FIX
from .checks import PageChecker, stylesheet_findings
from .css import Cascade, parse_stylesheet
from .dom import parse_html
from .model import Finding

SKIP_DIRS = {"node_modules", ".git", ".next", "__pycache__"}


@dataclass
class SiteContext:
    unresolved: set = field(default_factory=set)


@dataclass
class ScanResult:
    root: str
    pages: list
    findings: list
    stylesheets: list
    remote_styles: list
    missing_styles: list
    unsupported_css: list
    technologies: list = field(default_factory=list)


def find_pages(root):
    pages = []
    for dirpath, dirs, files in os.walk(root):
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS and not d.startswith("."))
        for f in sorted(files):
            if f.lower().endswith((".html", ".htm")):
                pages.append(os.path.join(dirpath, f))
    return pages


def _read(path):
    with open(path, encoding="utf-8", errors="replace") as fh:
        return fh.read()


def scan(root):
    root = os.path.abspath(root)
    if os.path.isfile(root):
        pages, root = [root], os.path.dirname(root)
    else:
        pages = find_pages(root)
    sheet_cache, remote, missing = {}, set(), set()
    findings, parsed_sheets, unsupported = [], [], set()
    ctx = SiteContext()

    def load_sheet(path):
        if path not in sheet_cache:
            rules = parse_stylesheet(_read(path), os.path.relpath(path, root))
            sheet_cache[path] = rules
            parsed_sheets.append(rules)
        return sheet_cache[path]

    inline_seen = 0
    titles = {}
    tech = {"HTML"}
    for page in pages:
        rel = os.path.relpath(page, root)
        tree = parse_html(_read(page))
        rules = []
        for node in tree.walk():
            if node.tag == "link" and "stylesheet" in (node.get("rel") or "").lower() and node.get("href"):
                href = node.get("href")
                parsed = urlparse(href)
                if parsed.scheme or href.startswith("//"):
                    remote.add(href)
                    continue
                target = unquote(parsed.path)
                base = root if target.startswith("/") else os.path.dirname(page)
                path = os.path.normpath(os.path.join(base, target.lstrip("/")))
                if os.path.isfile(path) and path.startswith(root):
                    rules.extend(load_sheet(path))
                else:
                    missing.add(f"{rel}: {href}")
            elif node.tag == "style":
                inline_seen += 1
                parsed_rules = parse_stylesheet(node.text(), rel, order_start=100000 * inline_seen)
                rules.extend(parsed_rules)
                parsed_sheets.append(parsed_rules)
        for node in tree.walk():
            if node.tag == "script":
                tech.add("JavaScript")
            if any(k == "role" or k.startswith("aria-") for k in node.attrs):
                tech.add("WAI-ARIA")
        if rules:
            tech.add("CSS")
        cascade = Cascade(rules, tree)
        page_findings = PageChecker(tree, cascade, rel, ctx).run()
        unsupported |= cascade.unsupported
        titles.setdefault(_title(tree), []).append(rel)
        findings.extend(page_findings)

    for rules in parsed_sheets:
        findings.extend(stylesheet_findings(rules))
    for title, files in titles.items():
        if title and len(files) >= 3:
            for f in files[1:]:
                findings.append(Finding("duplicate-title", "2.4.2", "A", "review", f, 0,
                                        f'Same <title> "{title}" as {len(files) - 1} other page(s): titles should tell pages apart.'))
    return ScanResult(root, [os.path.relpath(p, root) for p in pages], findings,
                      sorted(os.path.relpath(p, root) for p in sheet_cache),
                      sorted(remote), sorted(missing), sorted(unsupported),
                      sorted(tech, key=["HTML", "CSS", "JavaScript", "WAI-ARIA"].index))


def _title(tree):
    node = next((n for n in tree.walk() if n.tag == "title"), None)
    return " ".join(node.text().split()) if node else ""


def group(findings):
    """Collapse identical findings repeated across pages (templates)."""
    groups = {}
    for f in findings:
        key = (f.rule, f.kind, f.message)
        g = groups.setdefault(key, {"first": f, "locations": []})
        g["locations"].append((f.file, f.line))
    out = []
    for g in groups.values():
        f = g["first"]
        locs = sorted(g["locations"])
        out.append({"rule": f.rule, "wcag": f.wcag, "level": f.level, "kind": f.kind,
                    "message": f.message, "fix": FIX.get(f.rule, ""), "snippet": f.snippet, "locations": locs,
                    "pages": len({p for p, _ in locs})})
    out.sort(key=lambda g: (g["kind"] != "fail", g["wcag"], g["rule"], -g["pages"]))
    return out
