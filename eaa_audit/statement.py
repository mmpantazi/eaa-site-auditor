"""Draft the accessibility statement from scan results and a small config file."""

import datetime
from html import escape

from .i18n import AUTHORITY_HINT, MANUAL_LOCAL, NATIONAL_LAW, SC_NAMES, T
from .report import summary
from .scanner import group

TODO = "[TODO: {}]"

LANGS = set(T)


def starter_config(lang="en"):
    return {
        "language": lang,
        "organisation": TODO.format("legal name of the website owner"),
        "website_url": TODO.format("https://example.eu"),
        "contact_email": TODO.format("accessibility contact e-mail"),
        "contact_phone": "",
        "contact_address": "",
        "response_days": 14,
        "review_months": 12,
        "alternatives": [],
        "microenterprise": False,
        "national_law": NATIONAL_LAW[lang],
        "enforcement_authority": TODO.format(AUTHORITY_HINT[lang]),
        "measures": [],
        "manual_review_done": False,
        "manual_reviewer": "",
        "date": "",
    }


def _field(cfg, key, label, todos):
    v = (cfg.get(key) or "").strip() if isinstance(cfg.get(key), str) else cfg.get(key)
    if not v:
        todos.append(label)
        return TODO.format(label)
    if "[TODO" in str(v):
        todos.append(label)
    return v


def build_blocks(result, cfg, lang):
    t = T[lang]
    todos = []
    org = _field(cfg, "organisation", "organisation", todos)
    site = _field(cfg, "website_url", "website_url", todos)
    s = summary(result)
    groups = group(result.findings)
    fails = [g for g in groups if g["kind"] == "fail"]
    reviews = [g for g in groups if g["kind"] == "review" and g["wcag"] != "-"]
    manual_done = bool(cfg.get("manual_review_done"))
    full = manual_done and not fails
    today = cfg.get("date") or datetime.date.today().isoformat()

    intro = t["intro"].format(org=org, site=site)
    if cfg.get("national_law"):
        intro += " " + t["law"].format(law=cfg["national_law"])
    blocks = [("h1", t["title"].format(org=org)),
              ("p", intro),
              ("h2", t["h_status"]),
              ("p", t["status_full" if full else "status_partial"].format(site=site)),
              ("h2", t["h_limits"])]
    names = SC_NAMES[lang]
    by_sc = {}
    for g in fails:
        e = by_sc.setdefault(g["wcag"], [0, set()])
        e[0] += len(g["locations"])
        e[1].update(p for p, _ in g["locations"])
    if by_sc:
        blocks.append(("p", t["limits_intro"]))
        blocks.append(("ul", [t["limit_line"].format(sc=sc, name=names.get(sc, ""), n=n, pages=len(p)).replace(": :", ":")
                              for sc, (n, p) in sorted(by_sc.items(), key=lambda kv: [int(x) for x in kv[0].split(".")])]))
    else:
        blocks.append(("p", t["limits_none"]))
    rsc = sorted({g["wcag"] for g in reviews}, key=lambda x: [int(i) for i in x.split(".")])
    if rsc:
        blocks.append(("p", t["review_intro"]))
        blocks.append(("ul", [f"{sc} {names.get(sc, '')}".strip() for sc in rsc]))
    alts = [a for a in cfg.get("alternatives", []) if a]
    if alts:
        blocks += [("p", t["alts"]), ("ul", alts)]
    state = t["manual_done"] if manual_done else t["manual_todo"]
    blocks.append(("p", t["manual_intro"].format(state=state)))
    blocks.append(("ul", MANUAL_LOCAL[lang]))
    if cfg.get("microenterprise"):
        blocks += [("h2", t["h_micro"]), ("p", t["micro"].format(org=org))]
    measures = [m for m in cfg.get("measures", []) if m] or [t["measures_default"]]
    blocks += [("h2", t["h_measures"]), ("ul", measures)]
    contact = []
    email = _field(cfg, "contact_email", "contact_email", todos)
    contact.append(t["contact_email"].format(v=email))
    if cfg.get("contact_phone"):
        contact.append(t["contact_phone"].format(v=cfg["contact_phone"]))
    if cfg.get("contact_address"):
        contact.append(t["contact_addr"].format(v=cfg["contact_address"]))
    days = cfg.get("response_days") or 14
    blocks += [("h2", t["h_feedback"]), ("p", t["feedback"].format(days=days)), ("ul", contact)]
    auth = _field(cfg, "enforcement_authority", "enforcement_authority", todos)
    blocks += [("h2", t["h_enforce"]), ("p", t["enforce"].format(auth=auth))]
    manual = t["prep_manual"].format(who=cfg.get("manual_reviewer") or "-") if manual_done else ""
    blocks += [("h2", t["h_prep"]),
               ("p", t["prep"].format(date=today, pages=s["pages"], manual=manual)),
               ("p", t["tech"].format(tech=", ".join(result.technologies))),
               ("p", t["review"].format(months=cfg.get("review_months") or 12))]
    return blocks, len(todos)


def render(result, cfg, lang, fmt):
    blocks, todos = build_blocks(result, cfg, lang)
    if fmt == "md":
        out = []
        for kind, val in blocks:
            if kind == "h1":
                out.append(f"# {val}\n")
            elif kind == "h2":
                out.append(f"## {val}\n")
            elif kind == "p":
                out.append(f"{val}\n")
            else:
                out.append("\n".join(f"- {i}" for i in val) + "\n")
        return "\n".join(out), todos
    body = []
    for kind, val in blocks:
        if kind in ("h1", "h2", "p"):
            body.append(f"<{kind}>{escape(val)}</{kind}>")
        else:
            body.append("<ul>" + "".join(f"<li>{escape(i)}</li>" for i in val) + "</ul>")
    title = next(v for k, v in blocks if k == "h1")
    html = f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)}</title>
<style>
body{{font:1rem/1.6 system-ui,sans-serif;color:#1a1a1a;background:#fff;max-width:44rem;margin:0 auto;padding:1rem}}
</style>
</head>
<body>
<main>
{chr(10).join(body)}
</main>
</body>
</html>
"""
    return html, todos
