"""Minimal HTML tree built on html.parser, keeping source line numbers."""

from html.parser import HTMLParser

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link",
        "meta", "param", "source", "track", "wbr"}


class Node:
    __slots__ = ("tag", "attrs", "children", "parent", "line", "_text")

    def __init__(self, tag, attrs=None, parent=None, line=0):
        self.tag = tag
        self.attrs = attrs or {}
        self.children = []
        self.parent = parent
        self.line = line
        self._text = None

    def get(self, name, default=None):
        return self.attrs.get(name, default)

    def has(self, name):
        return name in self.attrs

    def classes(self):
        return (self.attrs.get("class") or "").split()

    def walk(self):
        yield self
        for child in self.children:
            if isinstance(child, Node):
                yield from child.walk()

    def ancestors(self):
        node = self.parent
        while node is not None:
            yield node
            node = node.parent

    def own_text(self):
        return "".join(c for c in self.children if isinstance(c, str))

    def text(self):
        parts = []
        for c in self.children:
            parts.append(c if isinstance(c, str) else c.text())
        return "".join(parts)

    def snippet(self, limit=110):
        attrs = "".join(
            f' {k}="{v}"' if v is not None else f" {k}" for k, v in self.attrs.items()
        )
        out = f"<{self.tag}{attrs}>"
        return out if len(out) <= limit else out[: limit - 1] + "…"


class _Builder(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node("#document")
        self.cur = self.root

    def handle_starttag(self, tag, attrs):
        node = Node(tag, {k: v for k, v in attrs}, self.cur, self.getpos()[0])
        self._autoclose(tag)
        node.parent = self.cur
        self.cur.children.append(node)
        if tag not in VOID:
            self.cur = node

    def handle_startendtag(self, tag, attrs):
        node = Node(tag, {k: v for k, v in attrs}, self.cur, self.getpos()[0])
        self.cur.children.append(node)

    def handle_endtag(self, tag):
        node = self.cur
        while node is not self.root:
            if node.tag == tag:
                self.cur = node.parent
                return
            node = node.parent

    def handle_data(self, data):
        self.cur.children.append(data)

    def _autoclose(self, tag):
        closers = {"li": {"li"}, "p": {"p"}, "option": {"option"},
                   "tr": {"tr", "td", "th"}, "td": {"td", "th"}, "th": {"td", "th"},
                   "dt": {"dt", "dd"}, "dd": {"dt", "dd"}}
        if tag in closers and self.cur.tag in closers[tag]:
            self.cur = self.cur.parent
        if tag in {"div", "ul", "ol", "table", "h1", "h2", "h3", "h4", "h5", "h6"} \
                and self.cur.tag == "p":
            self.cur = self.cur.parent


def parse_html(source):
    builder = _Builder()
    builder.feed(source)
    builder.close()
    return builder.root
