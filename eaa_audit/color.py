"""CSS colour parsing and WCAG contrast maths."""

import colorsys
import re

NAMED = {
    "black": (0, 0, 0), "white": (255, 255, 255), "red": (255, 0, 0),
    "green": (0, 128, 0), "blue": (0, 0, 255), "yellow": (255, 255, 0),
    "gray": (128, 128, 128), "grey": (128, 128, 128), "silver": (192, 192, 192),
    "orange": (255, 165, 0), "purple": (128, 0, 128), "navy": (0, 0, 128),
    "teal": (0, 128, 128), "maroon": (128, 0, 0), "lime": (0, 255, 0),
    "aqua": (0, 255, 255), "cyan": (0, 255, 255), "fuchsia": (255, 0, 255),
    "magenta": (255, 0, 255), "olive": (128, 128, 0), "pink": (255, 192, 203),
    "brown": (165, 42, 42), "gold": (255, 215, 0), "lightgray": (211, 211, 211),
    "lightgrey": (211, 211, 211), "darkgray": (169, 169, 169),
    "darkgrey": (169, 169, 169), "dimgray": (105, 105, 105),
    "whitesmoke": (245, 245, 245), "lightblue": (173, 216, 230),
    "darkblue": (0, 0, 139), "darkgreen": (0, 100, 0), "darkred": (139, 0, 0),
    "crimson": (220, 20, 60), "coral": (255, 127, 80), "tomato": (255, 99, 71),
    "salmon": (250, 128, 114), "khaki": (240, 230, 140), "ivory": (255, 255, 240),
    "beige": (245, 245, 220), "lightyellow": (255, 255, 224),
    "lightgreen": (144, 238, 144), "skyblue": (135, 206, 235),
    "royalblue": (65, 105, 225), "steelblue": (70, 130, 180),
    "slategray": (112, 128, 144), "slategrey": (112, 128, 144),
    "indigo": (75, 0, 130), "violet": (238, 130, 238), "gainsboro": (220, 220, 220),
    "darkorange": (255, 140, 0), "firebrick": (178, 34, 34),
}

_HEX = re.compile(r"^#([0-9a-f]{3,4}|[0-9a-f]{6}|[0-9a-f]{8})$", re.I)
_FUNC = re.compile(r"^(rgba?|hsla?)\((.*)\)$", re.I)


def parse_color(value):
    """Return (r, g, b, a) or None if the value is not a plain colour."""
    if not value:
        return None
    v = value.strip().lower()
    if v == "transparent":
        return (0, 0, 0, 0.0)
    if v in NAMED:
        return NAMED[v] + (1.0,)
    m = _HEX.match(v)
    if m:
        h = m.group(1)
        if len(h) in (3, 4):
            h = "".join(c * 2 for c in h)
        r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
        a = int(h[6:8], 16) / 255 if len(h) == 8 else 1.0
        return (r, g, b, a)
    m = _FUNC.match(v)
    if m:
        parts = [p for p in re.split(r"[\s,/]+", m.group(2).strip()) if p]
        if len(parts) < 3:
            return None
        try:
            alpha = _num(parts[3]) if len(parts) > 3 else 1.0
            if m.group(1).startswith("rgb"):
                r, g, b = (_chan(p) for p in parts[:3])
            else:
                h = float(parts[0].replace("deg", "")) % 360 / 360
                s, l = (float(p.rstrip("%")) / 100 for p in parts[1:3])
                r, g, b = (round(x * 255) for x in colorsys.hls_to_rgb(h, l, s))
            return (r, g, b, max(0.0, min(1.0, alpha)))
        except ValueError:
            return None
    return None


def find_color_token(value):
    for tok in re.findall(r"#[0-9a-fA-F]{3,8}|(?:rgba?|hsla?)\([^)]*\)|[a-zA-Z]+", value):
        if parse_color(tok):
            return tok
    return None


def _chan(p):
    return round(float(p[:-1]) * 2.55) if p.endswith("%") else round(float(p))


def _num(p):
    return float(p[:-1]) / 100 if p.endswith("%") else float(p)


def blend(fg, bg):
    """Composite fg (with alpha) over an opaque bg."""
    a = fg[3]
    return tuple(round(fg[i] * a + bg[i] * (1 - a)) for i in range(3)) + (1.0,)


def _lin(c):
    c /= 255
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def luminance(rgb):
    r, g, b = (_lin(c) for c in rgb[:3])
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(a, b):
    la, lb = luminance(a), luminance(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def to_hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(*rgb[:3])
