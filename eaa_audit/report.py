"""Render scan results as text, JSON or a self-contained accessible HTML page."""

import json
from html import escape

from .i18n import MANUAL_LOCAL
from .scanner import group

MANUAL_ONLY = MANUAL_LOCAL["en"]


def summary(result):
    groups = group(result.findings)
    return {
        "pages": len(result.pages),
        "stylesheets": len(result.stylesheets),
        "failures": sum(1 for g in groups if g["kind"] == "fail"),
        "failure_instances": sum(len(g["locations"]) for g in groups if g["kind"] == "fail"),
        "reviews": sum(1 for g in groups if g["kind"] == "review"),
        "remote_stylesheets": result.remote_styles,
        "missing_stylesheets": result.missing_styles,
        "ignored_css_rules": len(result.unsupported_css),
    }


def to_dict(result):
    return {"root": result.root, "summary": summary(result),
            "findings": group(result.findings), "manual_checks": MANUAL_ONLY}


def to_json(result):
    return json.dumps(to_dict(result), indent=2, ensure_ascii=False)


def to_text(result, color=False):
    s = summary(result)
    red, yel, dim, off = ("\033[31m", "\033[33m", "\033[2m", "\033[0m") if color else ("", "", "", "")
    lines = [f"Scanned {s['pages']} page(s), {s['stylesheets']} local stylesheet(s) in {result.root}", ""]
    for g in group(result.findings):
        tag = f"{red}FAIL  {off}" if g["kind"] == "fail" else f"{yel}REVIEW{off}"
        lvl = f"WCAG {g['wcag']} ({g['level']})" if g["wcag"] != "-" else "note"
        lines.append(f"{tag} {g['rule']}  {lvl}  on {g['pages']} page(s)")
        lines.append(f"       {g['message']}")
        if g["snippet"]:
            lines.append(f"       {dim}{g['snippet']}{off}")
        if g["fix"]:
            lines.append(f"       Fix: {g['fix']}")
        for f, ln in g["locations"][:3]:
            lines.append(f"       at {f}:{ln}")
        if len(g["locations"]) > 3:
            lines.append(f"       … and {len(g['locations']) - 3} more")
        lines.append("")
    if s["remote_stylesheets"]:
        lines.append(f"Note: {len(s['remote_stylesheets'])} remote stylesheet(s) were not fetched; contrast results may be incomplete.")
    if s["missing_stylesheets"]:
        lines.append(f"Note: {len(s['missing_stylesheets'])} linked stylesheet(s) not found in the folder.")
    if s["ignored_css_rules"]:
        lines.append(f"Note: {s['ignored_css_rules']} CSS rule(s) set colours with selectors this tool cannot evaluate (e.g. :nth-child(), :is()); contrast may be incomplete.")
    lines.append(f"Result: {s['failures']} failing issue type(s) ({s['failure_instances']} places), {s['reviews']} item(s) to review by hand.")
    lines.append("Automated checks find only part of all WCAG problems; see 'manual checks' in the HTML/JSON report.")
    return "\n".join(lines)


def to_html(result):
    s = summary(result)
    rows = []
    for g in group(result.findings):
        locs = "".join(f"<li><code>{escape(f)}:{ln}</code></li>" for f, ln in g["locations"][:5])
        more = f"<li>… and {len(g['locations']) - 5} more</li>" if len(g["locations"]) > 5 else ""
        kind = "Fail" if g["kind"] == "fail" else "Review"
        wcag = f"WCAG {g['wcag']} (level {g['level']})" if g["wcag"] != "-" else "Note"
        snippet = f"<p><code>{escape(g['snippet'])}</code></p>" if g["snippet"] else ""
        fix = f"<p><strong>Fix:</strong> {escape(g['fix'])}</p>" if g["fix"] else ""
        rows.append(f"<article><h3><span class=\"k {g['kind']}\">{kind}</span> {escape(g['rule'])}</h3>"
                    f"<p>{escape(wcag)}, {g['pages']} page(s)</p><p>{escape(g['message'])}</p>{snippet}{fix}"
                    f"<ul>{locs}{more}</ul></article>")
    manual = "".join(f"<li>{escape(m)}</li>" for m in MANUAL_ONLY)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Accessibility scan report</title>
<style>
body{{font:1rem/1.5 system-ui,sans-serif;color:#1a1a1a;background:#fff;max-width:56rem;margin:0 auto;padding:1rem}}
article{{border:1px solid #767676;border-radius:.4rem;padding:.5rem 1rem;margin:1rem 0}}
.k{{padding:.1rem .5rem;border-radius:.3rem;color:#fff;font-size:.9rem}}
.k.fail{{background:#a40000}} .k.review{{background:#6b4a00}}
code{{background:#f0f0f0;padding:0 .2rem;word-break:break-all}}
a:focus-visible{{outline:3px solid #0050b3;outline-offset:2px}}
</style>
</head>
<body>
<main>
<h1>Accessibility scan report</h1>
<p>{s['pages']} page(s) and {s['stylesheets']} stylesheet(s) scanned in <code>{escape(result.root)}</code>.
{s['failures']} failing issue type(s) in {s['failure_instances']} place(s); {s['reviews']} item(s) need a manual look.</p>
<h2>Findings</h2>
{''.join(rows) or '<p>No findings.</p>'}
<h2>Manual checks automation cannot do</h2>
<ul>{manual}</ul>
</main>
</body>
</html>
"""
