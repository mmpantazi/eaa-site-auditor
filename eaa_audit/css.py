"""Small CSS parser and cascade, enough to resolve text and background colours."""

import re
from dataclasses import dataclass, field

_COMMENT = re.compile(r"/\*.*?\*/", re.S)
_VAR = re.compile(r"var\(\s*(--[\w-]+)\s*(?:,\s*([^)]*))?\)")


@dataclass
class Rule:
    selector: str
    decls: dict
    source: str
    line: int
    order: int
    specificity: tuple = field(default=(0, 0, 0))


def _specificity(selector):
    ids = len(re.findall(r"#[\w-]+", selector))
    cls = len(re.findall(r"\.[\w-]+|\[[^\]]*\]|:(?!:)[\w-]+", selector))
    tags = len(re.findall(r"(?:^|[\s>+~])[a-zA-Z][\w-]*", selector))
    return (ids, cls, tags)


def parse_declarations(block):
    decls = {}
    for part in _split_top(block, ";"):
        if ":" not in part:
            continue
        name, _, value = part.partition(":")
        name = name.strip().lower()
        value = value.strip()
        important = bool(re.search(r"!\s*important\s*$", value, re.I))
        value = re.sub(r"\s*!\s*important\s*$", "", value, flags=re.I)
        if name:
            decls[name] = (value, important)
    return decls


def _split_top(text, sep):
    out, depth, cur = [], 0, []
    quote = None
    for ch in text:
        if quote:
            quote = None if ch == quote else quote
        elif ch in "\"'":
            quote = ch
        elif ch == "(":
            depth += 1
        elif ch == ")":
            depth = max(0, depth - 1)
        elif ch == sep and depth == 0:
            out.append("".join(cur))
            cur = []
            continue
        cur.append(ch)
    out.append("".join(cur))
    return out


def parse_stylesheet(text, source, order_start=0):
    """Return rules. Skips @font-face/@keyframes and dark-scheme/print media."""
    rules = []
    clean = _COMMENT.sub(lambda m: re.sub(r"[^\n]", " ", m.group(0)), text)
    order = [order_start]

    def walk(chunk, base_line):
        i, n = 0, len(chunk)
        while i < n:
            brace = chunk.find("{", i)
            if brace == -1:
                return
            prelude = chunk[i:brace].strip()
            depth, j = 1, brace + 1
            while j < n and depth:
                depth += {"{": 1, "}": -1}.get(chunk[j], 0)
                j += 1
            body = chunk[brace + 1:j - 1]
            line = base_line + chunk.count("\n", 0, brace)
            if prelude.startswith("@"):
                if prelude.startswith(("@media", "@supports", "@layer")) and \
                        _media_applies(prelude):
                    walk(body, line)
            else:
                decls = parse_declarations(body)
                for sel in _split_top(prelude, ","):
                    sel = " ".join(sel.split())
                    if sel:
                        order[0] += 1
                        rules.append(Rule(sel, decls, source, line, order[0],
                                          _specificity(sel)))
            i = j

    walk(clean, 1)
    return rules


def _media_applies(prelude):
    p = prelude.lower()
    return not re.search(r"prefers-color-scheme:\s*dark|print|prefers-reduced-motion|(min|max)-(width|height)", p)


_TOKEN = re.compile(
    r"""(?P<comb>\s*[>+~]\s*|\s+)|(?P<tag>\*|[a-zA-Z][\w-]*)|\.(?P<cls>[-\w]+)|"""
    r"""\#(?P<id>[-\w]+)|\[(?P<attr>[^\]]*)\]|(?P<pseudo>::?[\w-]+(?:\([^)]*\))?)"""
)


def _compile(selector):
    """Return list of (combinator, compound) or None when unsupported."""
    parts, comb, comp, pos = [], " ", {}, 0
    sel = selector.strip()
    while pos < len(sel):
        m = _TOKEN.match(sel, pos)
        if not m:
            return None
        pos = m.end()
        if m.group("comb") is not None:
            if comp:
                parts.append((comb, comp))
                comp = {}
            c = m.group("comb").strip()
            comb = c or " "
        elif m.group("tag"):
            comp["tag"] = m.group("tag").lower()
        elif m.group("cls"):
            comp.setdefault("cls", []).append(m.group("cls"))
        elif m.group("id"):
            comp["id"] = m.group("id")
        elif m.group("attr") is not None:
            comp.setdefault("attr", []).append(m.group("attr"))
        else:
            ps = m.group("pseudo")
            if ps.startswith(":not(") and ps.endswith(")"):
                inner = _compile(ps[5:-1])
                if not inner or len(inner) != 1:
                    return None
                comp.setdefault("not", []).append(inner[0][1])
                continue
            if ps.startswith("::") or ps.split("(")[0] not in (":root", ":first-child"):
                return None
            comp.setdefault("pseudo", []).append(ps)
    if comp:
        parts.append((comb, comp))
    return parts or None


def _match_compound(node, comp):
    if "tag" in comp and comp["tag"] != "*" and node.tag != comp["tag"]:
        return False
    if "id" in comp and node.get("id") != comp["id"]:
        return False
    if "cls" in comp:
        have = node.classes()
        if any(c not in have for c in comp["cls"]):
            return False
    for a in comp.get("attr", []):
        name, _, val = a.partition("=")
        name = name.strip().rstrip("~|^$*")
        if name not in node.attrs:
            return False
        if val and node.get(name) != val.strip().strip("\"'"):
            return False
    if any(_match_compound(node, neg) for neg in comp.get("not", [])):
        return False
    for ps in comp.get("pseudo", []):
        if ps == ":root" and node.tag != "html":
            return False
        if ps == ":first-child" and (node.parent is None or
                                     next((c for c in node.parent.children
                                           if not isinstance(c, str)), None) is not node):
            return False
    return True


def _previous_siblings(node):
    if node.parent is None:
        return []
    kids = [c for c in node.parent.children if not isinstance(c, str)]
    return kids[:kids.index(node)][::-1]


def _bucket_key(comp):
    if "id" in comp:
        return ("id", comp["id"])
    if "cls" in comp:
        return ("cls", comp["cls"][0])
    if comp.get("tag", "*") != "*":
        return ("tag", comp["tag"])
    return None


def matches(node, compiled):
    def rec(n, idx):
        comb, comp = compiled[idx]
        if not _match_compound(n, comp):
            return False
        if idx == 0:
            return True
        prev_comb = compiled[idx][0]
        if prev_comb in ("+", "~"):
            sibs = _previous_siblings(n)
            if prev_comb == "+":
                return bool(sibs) and rec(sibs[0], idx - 1)
            return any(rec(x, idx - 1) for x in sibs)
        if prev_comb == ">":
            return n.parent is not None and rec(n.parent, idx - 1)
        return any(rec(a, idx - 1) for a in n.ancestors())
    return rec(node, len(compiled) - 1)


_SIZE = re.compile(r"^([\d.]+)(px|rem|em|pt|%)$")
_FONT_SHORTHAND_SIZE = re.compile(r"(?:^|\s)([\d.]+(?:px|rem|em|pt|%))(?:/\S+)?(?:\s|$)")


def _sets_colour(decls):
    return any(k in decls for k in ("color", "background", "background-color"))


def _is_state_selector(selector):
    return bool(re.search(r":(hover|focus|active|visited|focus-visible|focus-within|disabled|checked)|::", selector))


def _expand_font(decl):
    short = decl.get("font")
    if short:
        size = _FONT_SHORTHAND_SIZE.search(short)
        weight = re.search(r"\b(bold|bolder|[1-9]00)\b", short)
        if size:
            decl.setdefault("font-size", size.group(1))
        if weight:
            decl.setdefault("font-weight", weight.group(1))
    return decl


def _font_px(value, parent_px):
    base = float(parent_px[:-2]) if parent_px and parent_px.endswith("px") else 16.0
    m = _SIZE.match((value or "").strip().lower())
    if not m:
        return f"{base:g}px"
    n, unit = float(m.group(1)), m.group(2)
    px = {"px": n, "rem": n * 16, "em": n * base, "pt": n * 96 / 72, "%": n * base / 100}[unit]
    return f"{px:g}px"


class Cascade:
    """Computes style properties for nodes of one document."""

    INHERITED = {"color", "font-size", "font-weight", "visibility"}

    def __init__(self, rules, root):
        self.buckets = {}
        self.unsupported = set()
        for r in rules:
            compiled = _compile(r.selector)
            if compiled:
                self.buckets.setdefault(_bucket_key(compiled[-1][1]), []).append((r, compiled))
            elif _sets_colour(r.decls) and not _is_state_selector(r.selector):
                self.unsupported.add((r.source, r.selector))
        self.root = root
        self._cache = {}

    def declared(self, node):
        found = []
        keys = [None, ("tag", node.tag)] + [("cls", c) for c in node.classes()]
        if node.get("id"):
            keys.append(("id", node.get("id")))
        candidates = [rc for k in keys for rc in self.buckets.get(k, ())]
        for r, compiled in candidates:
            if matches(node, compiled):
                for name, (value, imp) in r.decls.items():
                    found.append(((imp, r.specificity, r.order), name, value))
        inline = node.get("style")
        if inline:
            for name, (value, imp) in parse_declarations(inline).items():
                found.append(((imp, (1, 0, 0, 0), 10**9), name, value))
        found.sort(key=lambda x: x[0])
        out = {}
        for _, name, value in found:
            out[name] = value
        return out

    def style(self, node):
        key = id(node)
        if key in self._cache:
            return self._cache[key]
        parent_style = self.style(node.parent) if node.parent is not None \
            and node.parent.tag != "#document" else {}
        decl = _expand_font(self.declared(node))
        if node.tag == "a" and node.has("href") and "color" not in decl:
            decl["color"] = "#0000ee"
        computed = {}
        for name in self.INHERITED:
            if name in parent_style:
                computed[name] = parent_style[name]
        for name, value in decl.items():
            computed[name] = value
        for name, value in parent_style.items():
            if name.startswith("--") and name not in decl:
                computed[name] = value
        for name in list(computed):
            computed[name] = self._resolve_vars(computed[name], computed)
        computed["font-size"] = _font_px(computed.get("font-size"), parent_style.get("font-size"))
        if "color" in computed and computed["color"].strip().lower() in ("inherit", "currentcolor"):
            computed["color"] = parent_style.get("color", "")
        self._cache[key] = computed
        return computed

    def _resolve_vars(self, value, computed, depth=0):
        if "var(" not in value or depth > 8:
            return value

        def sub(m):
            got = computed.get(m.group(1))
            if got is None:
                return m.group(2).strip() if m.group(2) else "var-unresolved"
            return self._resolve_vars(got, computed, depth + 1)

        return _VAR.sub(sub, value)
