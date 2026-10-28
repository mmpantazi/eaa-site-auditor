"""Static WCAG 2.2 checks on one parsed page."""

import re

from . import color as C
from .css import Cascade
from .model import Finding

FORM_SKIP = {"hidden", "submit", "button", "reset", "image"}
GENERIC_LINK = {
    "click here", "here", "read more", "more", "learn more", "link", "this",
    "klik hier", "hier", "mehr", "mehr lesen", "weiterlesen", "aici", "mai mult",
    "citește mai mult", "citeste mai mult", "en savoir plus", "cliquez ici", "ici",
}
FILENAME_ALT = re.compile(r"(\.(jpe?g|png|gif|svg|webp|avif)$|^(img|image|dsc|photo|picture)[-_ ]?\d*$)", re.I)
LANG_OK = re.compile(r"^[a-zA-Z]{2,3}(-[a-zA-Z0-9]{2,8})*$")
ARIA_ROLES = {
    "alert", "alertdialog", "application", "article", "banner", "button", "cell",
    "checkbox", "columnheader", "combobox", "complementary", "contentinfo",
    "definition", "dialog", "directory", "document", "feed", "figure", "form",
    "grid", "gridcell", "group", "heading", "img", "link", "list", "listbox",
    "listitem", "log", "main", "marquee", "math", "menu", "menubar", "menuitem",
    "menuitemcheckbox", "menuitemradio", "navigation", "none", "note", "option",
    "presentation", "progressbar", "radio", "radiogroup", "region", "row",
    "rowgroup", "rowheader", "scrollbar", "search", "searchbox", "separator",
    "slider", "spinbutton", "status", "switch", "tab", "table", "tablist",
    "tabpanel", "term", "textbox", "timer", "toolbar", "tooltip", "tree",
    "treegrid", "treeitem", "generic", "code", "emphasis", "strong", "paragraph",
    "blockquote", "caption", "deletion", "insertion", "meter", "subscript",
    "superscript", "time", "mark", "suggestion", "comment", "associationlist",
}
AUTOCOMPLETE_HINT = re.compile(r"(e-?mail|phone|tel|first.?name|last.?name|postcode|zip|street|address|city)", re.I)


def _norm(s):
    return " ".join((s or "").split())


class PageChecker:
    def __init__(self, root, cascade, path, site_ctx):
        self.root = root
        self.cascade = cascade
        self.path = path
        self.ctx = site_ctx
        self.findings = []
        self.nodes = [n for n in root.walk() if n.tag != "#document"]
        self.ids = {}
        for n in self.nodes:
            i = n.get("id")
            if i:
                self.ids.setdefault(i, []).append(n)

    def add(self, rule, wcag, level, kind, node, message):
        self.findings.append(Finding(rule, wcag, level, kind, self.path,
                                     node.line if node else 0, message,
                                     node.snippet() if node else ""))

    def run(self):
        for fn in (self.document, self.images, self.forms, self.names, self.headings,
                   self.landmarks, self.aria, self.media, self.tables,
                   self.interaction, self.contrast, self.targets):
            fn()
        return self.findings

    def by_tag(self, *tags):
        return [n for n in self.nodes if n.tag in tags]

    def hidden(self, node):
        for n in [node, *node.ancestors()]:
            if n.tag == "#document":
                continue
            if n.has("hidden") or n.get("aria-hidden") == "true":
                return True
            st = self.cascade.style(n)
            if st.get("display", "").strip() == "none" or st.get("visibility", "").strip() == "hidden":
                return True
        return False

    def accessible_name(self, node, _seen=None):
        if node.get("aria-labelledby"):
            ids = node.get("aria-labelledby").split()
            txt = " ".join(_norm(self._text_of(self.ids[i][0])) for i in ids if i in self.ids)
            if txt:
                return txt
        if _norm(node.get("aria-label")):
            return _norm(node.get("aria-label"))
        if node.tag == "input" and node.get("type", "text").lower() in {"submit", "button", "reset"}:
            return _norm(node.get("value")) or ("Submit" if node.get("type") == "submit" else "")
        if node.tag == "input" and node.get("type", "").lower() == "image":
            return _norm(node.get("alt"))
        text = _norm(self._text_of(node))
        if text:
            return text
        return _norm(node.get("title"))

    def _text_of(self, node):
        parts = []
        for c in node.children:
            if isinstance(c, str):
                parts.append(c)
            elif c.tag in ("script", "style"):
                continue
            elif c.tag == "img":
                parts.append(c.get("alt") or "")
            elif c.tag == "svg":
                t = next((x for x in c.walk() if x.tag == "title"), None)
                parts.append(_norm(c.get("aria-label")) or (t.text() if t else ""))
            elif c.get("aria-hidden") == "true":
                continue
            else:
                parts.append(self._text_of(c))
        return " ".join(parts)

    def document(self):
        html = next((n for n in self.nodes if n.tag == "html"), None)
        if html is None:
            return
        lang = html.get("lang") or html.get("xml:lang")
        if not lang or not lang.strip():
            self.add("html-lang", "3.1.1", "A", "fail", html, "<html> has no lang attribute; screen readers cannot pick the right voice.")
        elif not LANG_OK.match(lang.strip()):
            self.add("html-lang", "3.1.1", "A", "fail", html, f'lang="{lang}" is not a valid language tag.')
        title = next((n for n in self.nodes if n.tag == "title"), None)
        if title is None or not _norm(title.text()):
            self.add("document-title", "2.4.2", "A", "fail", title or html, "Page has no (or an empty) <title>.")
        for m in self.by_tag("meta"):
            name = (m.get("name") or "").lower()
            content = (m.get("content") or "").lower()
            if name == "viewport":
                if re.search(r"user-scalable\s*=\s*(no|0)", content):
                    self.add("viewport-zoom", "1.4.4", "AA", "fail", m, "Viewport disables pinch zoom (user-scalable=no).")
                mx = re.search(r"maximum-scale\s*=\s*([\d.]+)", content)
                if mx and float(mx.group(1)) < 2:
                    self.add("viewport-zoom", "1.4.4", "AA", "fail", m, f"maximum-scale={mx.group(1)} stops users zooming to 200%.")
            if (m.get("http-equiv") or "").lower() == "refresh":
                delay = re.match(r"\s*(\d+)", content)
                if delay and int(delay.group(1)) > 0:
                    self.add("meta-refresh", "2.2.1", "A", "fail", m, "Timed meta refresh redirects or reloads without user control.")
        for n in self.by_tag("marquee", "blink"):
            self.add("moving-content", "2.2.2", "A", "fail", n, f"<{n.tag}> creates moving content users cannot pause.")
        body = next((n for n in self.nodes if n.tag == "body"), None)
        if body is not None and len(_norm(body.text())) < 20 and any(n.tag == "script" for n in self.nodes):
            self.add("client-rendered", "-", "-", "review", body, "Body has almost no HTML text but loads scripts: content is probably rendered in the browser and was not scanned.")

    def images(self):
        for n in self.by_tag("img"):
            if n.get("role") in ("presentation", "none") or self.hidden(n):
                continue
            if not n.has("alt"):
                self.add("img-alt", "1.1.1", "A", "fail", n, "Image has no alt attribute (use alt=\"\" if decorative).")
            elif FILENAME_ALT.search(_norm(n.get("alt"))):
                self.add("img-alt-filename", "1.1.1", "A", "review", n, "alt text looks like a file name, not a description.")
        for n in self.by_tag("input"):
            if n.get("type", "").lower() == "image" and not _norm(n.get("alt")) and not n.get("aria-label"):
                self.add("input-image-alt", "1.1.1", "A", "fail", n, "Image button has no alt text.")
        for n in self.by_tag("area"):
            if n.has("href") and not _norm(n.get("alt")) and not n.get("aria-label"):
                self.add("area-alt", "1.1.1", "A", "fail", n, "Image-map area has no alt text.")
        for n in self.by_tag("svg"):
            if n.get("role") == "img" and not self.accessible_name(n):
                self.add("svg-img-alt", "1.1.1", "A", "fail", n, "SVG with role=\"img\" has no accessible name.")

    def forms(self):
        labels_for = {n.get("for") for n in self.by_tag("label") if n.get("for")}
        for lab in self.by_tag("label"):
            f = lab.get("for")
            if f and f not in self.ids:
                self.add("label-target", "1.3.1", "A", "fail", lab, f'<label for="{f}"> points to an id that does not exist.')
        for n in self.by_tag("input", "select", "textarea"):
            typ = n.get("type", "text").lower()
            if n.tag == "input" and typ in FORM_SKIP or self.hidden(n):
                continue
            named = (n.get("id") in labels_for if n.get("id") else False) \
                or any(a.tag == "label" for a in n.ancestors()) \
                or _norm(n.get("aria-label")) or n.get("aria-labelledby") or _norm(n.get("title"))
            if not named:
                hint = " A placeholder is not a label." if n.get("placeholder") else ""
                self.add("form-label", "3.3.2", "A", "fail", n, "Form field has no programmatic label." + hint)
            ident = " ".join(filter(None, [n.get("name"), n.get("id"), typ if typ in ("email", "tel") else ""]))
            if n.tag == "input" and typ in ("text", "email", "tel", "") and not n.has("autocomplete") \
                    and AUTOCOMPLETE_HINT.search(ident):
                self.add("autocomplete", "1.3.5", "AA", "review", n, "Field collects personal data but has no autocomplete attribute.")
            if typ == "password" and n.get("autocomplete") == "off":
                self.add("auth-autocomplete", "3.3.8", "AA", "review", n, "Password field disables autocomplete; check that password managers still work.")
            if n.get("onpaste") and re.search(r"return\s+false|preventDefault", n.get("onpaste")):
                self.add("auth-paste", "3.3.8", "AA", "fail", n, "Field blocks pasting, which breaks password managers.")

    def names(self):
        for n in self.by_tag("a"):
            if not n.has("href") or self.hidden(n):
                continue
            name = self.accessible_name(n)
            if not name:
                self.add("link-name", "2.4.4", "A", "fail", n, "Link has no accessible name (empty text, no alt/aria-label).")
            elif name.lower().strip(" .:→»>") in GENERIC_LINK:
                self.add("link-purpose", "2.4.4", "A", "review", n, f'Link text "{name}" does not say where it goes.')
        for n in self.by_tag("button"):
            if not self.hidden(n) and not self.accessible_name(n):
                self.add("button-name", "4.1.2", "A", "fail", n, "Button has no accessible name.")
        for n in self.by_tag("input"):
            if n.get("type", "").lower() in ("submit", "button", "reset") and not self.accessible_name(n) \
                    and n.get("type").lower() != "submit":
                self.add("button-name", "4.1.2", "A", "fail", n, "Input button has no value/label.")
        for n in self.by_tag("iframe", "frame"):
            if not (_norm(n.get("title")) or n.get("aria-label")) and not self.hidden(n):
                self.add("frame-title", "4.1.2", "A", "fail", n, "Frame has no title.")
        for n in self.nodes:
            if n.get("role") in ("button", "link") and n.tag not in ("a", "button") and not self.accessible_name(n):
                self.add("role-name", "4.1.2", "A", "fail", n, f'Element with role="{n.get("role")}" has no accessible name.')

    def headings(self):
        hs = [n for n in self.nodes if re.fullmatch(r"h[1-6]", n.tag) and not self.hidden(n)]
        body = next((n for n in self.nodes if n.tag == "body"), None)
        if body is not None and not hs and len(_norm(body.text())) > 400:
            self.add("page-headings", "2.4.6", "AA", "review", body, "Long page with no headings: use <h1>–<h6> so screen reader users can navigate by section.")
        if body is not None and hs and not any(h.tag == "h1" for h in hs):
            self.add("page-h1", "2.4.6", "AA", "review", hs[0], "Page has headings but no <h1>.")
        prev = 0
        for h in hs:
            level = int(h.tag[1])
            if not _norm(self._text_of(h)) and not h.get("aria-label"):
                self.add("empty-heading", "2.4.6", "AA", "fail", h, "Heading is empty.")
            if prev and level > prev + 1:
                self.add("heading-order", "1.3.1", "A", "review", h, f"Heading jumps from h{prev} to h{level}.")
            prev = level

    def landmarks(self):
        has_main = any(n.tag == "main" or n.get("role") == "main" for n in self.nodes)
        body = next((n for n in self.nodes if n.tag == "body"), None)
        if body is None:
            return
        skip = any(n.tag == "a" and (n.get("href") or "").startswith("#") and len(n.get("href")) > 1
                   for n in list(body.walk())[:40])
        if not has_main and not skip:
            self.add("bypass-blocks", "2.4.1", "A", "fail", body, "No <main> landmark and no skip link: keyboard users must tab through the header on every page.")
        for key, nodes in self.ids.items():
            if len(nodes) > 1 and self._id_referenced(key):
                self.add("duplicate-id", "4.1.2", "A", "fail", nodes[1], f'id="{key}" is used more than once and is referenced by a label, ARIA attribute or anchor.')

    def _id_referenced(self, ident):
        for n in self.nodes:
            if n.get("for") == ident or n.get("href") == "#" + ident:
                return True
            for a in ("aria-labelledby", "aria-describedby", "aria-controls"):
                if ident in (n.get(a) or "").split():
                    return True
        return False

    def aria(self):
        focusable = lambda n: (n.tag in ("button", "select", "textarea") or (n.tag == "a" and n.has("href"))
                               or (n.tag == "input" and n.get("type") != "hidden")
                               or (n.has("tabindex") and (n.get("tabindex") or "").strip() not in ("-1",)))
        for n in self.nodes:
            if n.get("aria-hidden") == "true" and focusable(n) and not n.has("disabled"):
                self.add("aria-hidden-focus", "4.1.2", "A", "fail", n, "Focusable element has aria-hidden=\"true\".")
            role = n.get("role")
            if role and not all(r in ARIA_ROLES for r in role.lower().split()):
                self.add("aria-role", "4.1.2", "A", "fail", n, f'Unknown ARIA role "{role}".')
            for a in ("aria-labelledby", "aria-describedby"):
                for ref in (n.get(a) or "").split():
                    if ref not in self.ids:
                        self.add("aria-ref", "4.1.2", "A", "fail", n, f'{a} points to missing id "{ref}".')
            ti = (n.get("tabindex") or "").strip()
            if ti.lstrip("-").isdigit() and int(ti) > 0:
                self.add("tabindex-positive", "2.4.3", "A", "review", n, "Positive tabindex overrides the natural focus order.")

    def media(self):
        for n in self.by_tag("video", "audio"):
            tracks = [t for t in n.walk() if t.tag == "track"]
            kinds = {(t.get("kind") or "subtitles").lower() for t in tracks}
            if not kinds & {"captions", "subtitles"}:
                what = "captions" if n.tag == "video" else "a transcript"
                self.add("media-alternative", "1.2.2" if n.tag == "video" else "1.2.1", "A", "review", n, f"No <track> found; confirm {what} exist for this {n.tag}.")
            if n.has("autoplay") and not n.has("muted") and not n.has("controls"):
                self.add("autoplay", "1.4.2", "A", "fail", n, "Autoplaying sound with no controls.")

    def tables(self):
        for t in self.by_tag("table"):
            if t.get("role") in ("presentation", "none"):
                continue
            rows = [n for n in t.walk() if n.tag == "tr"]
            if len(rows) >= 2 and not any(n.tag == "th" for n in t.walk()):
                self.add("table-headers", "1.3.1", "A", "review", t, "Table has several rows but no <th> header cells (ignore if it is only for layout).")

    def interaction(self):
        for n in self.nodes:
            if re.search(r"\bblur\s*\(", n.get("onfocus") or ""):
                self.add("focus-blur", "2.4.7", "AA", "fail", n, "onfocus handler calls blur(): keyboard users can never rest focus on this element.")
            if n.get("draggable") == "true" or n.has("ondragstart"):
                self.add("dragging", "2.5.7", "AA", "review", n, "Draggable element: make sure there is a click or keyboard alternative.")
            if n.tag not in ("a", "button", "input", "select", "textarea", "summary") and (n.has("onclick")) \
                    and not n.has("tabindex") and not n.get("role"):
                self.add("click-no-keyboard", "2.1.1", "A", "fail", n, "onclick on a non-interactive element: not reachable by keyboard.")

    def _font_px(self, st):
        return float(st.get("font-size", "16px")[:-2])

    def _bg(self, node):
        """Return (rgb, culprit): culprit is the element that makes the background uncertain, if any."""
        layers = []
        culprit = None
        for n in [node, *node.ancestors()]:
            if n.tag == "#document":
                continue
            st = self.cascade.style(n)
            bgv = st.get("background-color") or ""
            short = st.get("background") or ""
            img = st.get("background-image", "") + " " + short
            c = C.parse_color(bgv) or (C.parse_color(_color_token(short)) if short else None)
            uncertain = "var-unresolved" in bgv + short or (bgv and C.parse_color(bgv) is None)
            if "gradient" in img or ("url(" in img and not ("no-repeat" in img and c)):
                uncertain = True
            if st.get("opacity") not in (None, "1") and n is not node:
                uncertain = True
            if uncertain and culprit is None:
                culprit = n
            if c and c[3] > 0:
                layers.append(c)
                if c[3] == 1:
                    break
        base = (255, 255, 255, 1.0)
        for layer in reversed(layers):
            base = C.blend(layer, base)
        return base, culprit

    def contrast(self):
        seen = set()
        for n in self.nodes:
            if n.tag in ("script", "style", "title", "head", "html", "body") or not n.own_text().strip():
                continue
            if n.has("disabled") or self.hidden(n):
                continue
            st = self.cascade.style(n)
            if any(a.has("disabled") for a in n.ancestors()):
                continue
            fg_raw = st.get("color", "")
            fg = C.parse_color(fg_raw) if fg_raw else (0, 0, 0, 1.0)
            if fg is None:
                if "var-unresolved" in fg_raw:
                    self.ctx.unresolved.add(self.path)
                continue
            bg, culprit = self._bg(n)
            if culprit is not None:
                if id(culprit) not in seen:
                    seen.add(id(culprit))
                    self.add("contrast-unknown", "1.4.3", "AA", "review", culprit, "Text sits on this gradient/image/semi-transparent layer: check contrast by hand.")
                continue
            fg = C.blend(fg, bg)
            ratio = C.contrast_ratio(fg, bg)
            size = self._font_px(st)
            weight = st.get("font-weight", "400").strip().lower()
            bold = weight in ("bold", "bolder") or (weight.isdigit() and int(weight) >= 700)
            large = size >= 24 or (bold and size >= 18.66)
            need = 3.0 if large else 4.5
            if ratio + 1e-9 < need:
                key = (C.to_hex(fg), C.to_hex(bg), large)
                if key in seen:
                    continue
                seen.add(key)
                self.add("color-contrast", "1.4.3", "AA", "fail", n,
                         f"Contrast {ratio:.2f}:1 ({C.to_hex(fg)} on {C.to_hex(bg)}), needs {need:g}:1.")

    def targets(self):
        for n in self.nodes:
            interactive = n.tag in ("button", "select") or (n.tag == "input" and n.get("type", "text") not in ("hidden",)) \
                or n.get("role") == "button" or (n.tag == "a" and n.has("href"))
            if not interactive or self.hidden(n):
                continue
            st = self.cascade.declared(n)
            if n.tag == "a" and st.get("display", "inline").strip() == "inline":
                continue
            dims = {}
            for prop in ("width", "height"):
                m = re.fullmatch(r"([\d.]+)px", st.get(prop, "").strip())
                if m:
                    dims[prop] = float(m.group(1))
            small = {k: v for k, v in dims.items() if v < 24}
            if small:
                desc = ", ".join(f"{k} {v:g}px" for k, v in small.items())
                self.add("target-size", "2.5.8", "AA", "review", n, f"Declared {desc}: pointer targets should be at least 24x24 CSS px unless spaced out.")


def _color_token(value):
    for tok in re.findall(r"#[0-9a-fA-F]{3,8}|(?:rgba?|hsla?)\([^)]*\)|[a-zA-Z]+", value):
        if C.parse_color(tok):
            return tok
    return None


def stylesheet_findings(rules, path_of):
    """Focus-visibility and sticky-obstruction checks over all rules of the site."""
    out = []
    removes = []
    has_focus_style = False
    for r in rules:
        d = {k: v[0].lower() for k, v in r.decls.items()}
        outline_off = d.get("outline", "") in ("none", "0", "0px") or d.get("outline-style") == "none" \
            or d.get("outline-width") in ("0", "0px")
        replaces = any(k in d for k in ("box-shadow", "border", "border-color", "text-decoration", "background", "background-color")) \
            or (d.get("outline", "") not in ("", "none", "0", "0px") and not outline_off) or "outline-color" in d
        focus_sel = ":focus" in r.selector
        if focus_sel and replaces and not outline_off:
            has_focus_style = True
        if focus_sel and replaces and outline_off:
            has_focus_style = True
        if outline_off:
            removes.append((r, focus_sel, replaces))
    for r, focus_sel, replaces in removes:
        if replaces and focus_sel:
            continue
        if focus_sel or not has_focus_style:
            out.append(Finding("focus-visible", "2.4.7", "AA", "fail", r.source, r.line,
                               "Focus outline removed and nothing replaces it: keyboard users cannot see where they are.",
                               r.selector + " { outline: none }"))
    for r in rules:
        d = {k: v[0].lower() for k, v in r.decls.items()}
        if re.search(r"(^|[\s>])a$", r.selector) and "none" in d.get("text-decoration", d.get("text-decoration-line", "")):
            out.append(Finding("link-underline", "1.4.1", "A", "review", r.source, r.line,
                               "Links lose their underline: if links sit inside running text they must differ from the text by more than colour (3:1 contrast plus another cue).",
                               r.selector))
            break
    fixed = [r for r in rules if r.decls.get("position", ("",))[0].lower() in ("fixed", "sticky")]
    scroll_pad = any("scroll-padding" in k or "scroll-margin" in k for r in rules for k in r.decls)
    if fixed and not scroll_pad:
        r = fixed[0]
        out.append(Finding("focus-obscured", "2.4.11", "AA", "review", r.source, r.line,
                           "Sticky/fixed element found and no scroll-padding set: tab through the page to confirm focused items are not hidden behind it.",
                           r.selector))
    return out
