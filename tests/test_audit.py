import atexit
import io
import json
import shutil
import os
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout

from eaa_audit import cli, color, report, statement
from eaa_audit.css import Cascade, parse_stylesheet
from eaa_audit.dom import parse_html
from eaa_audit.scanner import group, scan

GOOD_PAGE = """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><title>Home</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="s.css"></head>
<body><a href="#main" class="skip">Skip to content</a>
<header><nav><a href="/about">About us</a></nav></header>
<main id="main"><h1>Welcome</h1><h2>News</h2>
<img src="a.jpg" alt="A red bicycle leaning on a wall"><img src="d.png" alt="">
<form><label for="e">Email</label><input id="e" type="email" autocomplete="email">
<button type="submit">Send</button></form></main></body></html>"""
GOOD_CSS = "body{color:#222;background:#fff} a{color:#0033aa} a:focus{outline:2px solid #05f}"


def _tmp():
    d = tempfile.mkdtemp()
    atexit.register(shutil.rmtree, d, ignore_errors=True)
    return d


def make_site(files):
    d = _tmp()
    for name, content in files.items():
        path = os.path.join(d, name)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(content)
    return d


def rules_found(files, kind=None):
    res = scan(make_site(files))
    return {f.rule for f in res.findings if kind is None or f.kind == kind}


def page(body, head="", lang='lang="en"'):
    return f'<!DOCTYPE html><html {lang}><head><title>t</title>{head}</head><body><main>{body}</main></body></html>'


class ColorTests(unittest.TestCase):
    def test_contrast_black_white(self):
        self.assertAlmostEqual(color.contrast_ratio((0, 0, 0), (255, 255, 255)), 21, places=3)

    def test_known_ratio(self):
        self.assertAlmostEqual(color.contrast_ratio((119, 119, 119), (255, 255, 255)), 4.48, places=2)

    def test_parsers(self):
        self.assertEqual(color.parse_color("#fff"), (255, 255, 255, 1.0))
        self.assertEqual(color.parse_color("rgb(10, 20, 30)"), (10, 20, 30, 1.0))
        self.assertEqual(color.parse_color("rgba(0,0,0,.5)")[3], 0.5)
        self.assertEqual(color.parse_color("hsl(0, 100%, 50%)")[:3], (255, 0, 0))
        self.assertIsNone(color.parse_color("linear-gradient(red, blue)"))


class CssTests(unittest.TestCase):
    def style(self, css, html, finder):
        tree = parse_html(html)
        casc = Cascade(parse_stylesheet(css, "t.css"), tree)
        node = next(n for n in tree.walk() if finder(n))
        return casc.style(node)

    def test_specificity_and_inheritance(self):
        st = self.style("p{color:red} .a{color:blue} body{color:green}",
                        '<body><div><p class="a"><span>x</span></p></div></body>', lambda n: n.tag == "span")
        self.assertEqual(st["color"], "blue")

    def test_variables_and_descendant(self):
        st = self.style(":root{--c:#123456} .box p{color:var(--c)}",
                        '<html><body><div class="box"><p>x</p></div></body></html>', lambda n: n.tag == "p")
        self.assertEqual(st["color"], "#123456")

    def test_dark_scheme_media_ignored(self):
        st = self.style("p{color:#111} @media (prefers-color-scheme: dark){p{color:#fff}}",
                        "<p>x</p>", lambda n: n.tag == "p")
        self.assertEqual(st["color"], "#111")

    def test_width_conditional_media_not_flattened(self):
        st = self.style("p{color:#111} @media (max-width: 600px){p{color:#fff}}",
                        "<p>x</p>", lambda n: n.tag == "p")
        self.assertEqual(st["color"], "#111")

    def test_not_and_sibling_selectors(self):
        html = '<div><h2>t</h2><p class="a">x</p><p class="b">y</p></div>'
        st = self.style("p:not(.a){color:red} h2 + p{background:#111} h2 ~ p.b{border:0}", html, lambda n: n.get("class") == "b")
        self.assertEqual(st["color"], "red")
        a = self.style("p:not(.a){color:red} h2 + p{background-color:#111}", html, lambda n: n.get("class") == "a")
        self.assertNotIn("color", a)
        self.assertEqual(a["background-color"], "#111")

    def test_important_wins(self):
        st = self.style("p{color:red!important} #i{color:blue}", '<p id="i">x</p>', lambda n: n.tag == "p")
        self.assertEqual(st["color"], "red")


class RuleTests(unittest.TestCase):
    def test_clean_site_has_no_failures(self):
        self.assertEqual(rules_found({"index.html": GOOD_PAGE, "s.css": GOOD_CSS}, "fail"), set())

    def test_missing_alt(self):
        self.assertIn("img-alt", rules_found({"i.html": page('<img src="a.png">')}, "fail"))

    def test_empty_alt_and_presentation_ok(self):
        self.assertNotIn("img-alt", rules_found({"i.html": page('<img src="a.png" alt=""><img role="presentation" src="b">')}))

    def test_filename_alt_is_review(self):
        self.assertIn("img-alt-filename", rules_found({"i.html": page('<img src="a.png" alt="DSC_0012">')}, "review"))

    def test_lang_title(self):
        r = rules_found({"i.html": '<html><head></head><body><main>x</main></body></html>'}, "fail")
        self.assertTrue({"html-lang", "document-title"} <= r)

    def test_invalid_lang(self):
        self.assertIn("html-lang", rules_found({"i.html": page("x", lang='lang="english please"')}, "fail"))

    def test_form_label_variants(self):
        ok = page('<label>Name <input></label><input aria-label="Q"><label for="a">A</label><input id="a">')
        self.assertNotIn("form-label", rules_found({"i.html": ok}))
        bad = page('<input placeholder="Email">')
        self.assertIn("form-label", rules_found({"i.html": bad}, "fail"))

    def test_button_and_link_names(self):
        r = rules_found({"i.html": page('<button></button><a href="/x"><i class="icon"></i></a>')}, "fail")
        self.assertTrue({"button-name", "link-name"} <= r)
        ok = page('<button aria-label="Close"></button><a href="/x"><img src="l.png" alt="Home"></a>')
        self.assertEqual({"button-name", "link-name"} & rules_found({"i.html": ok}), set())

    def test_generic_link_text(self):
        self.assertIn("link-purpose", rules_found({"i.html": page('<a href="/x">Read more</a>')}, "review"))

    def test_heading_issues(self):
        r = rules_found({"i.html": page("<h2>A</h2><h4>B</h4><h3></h3>")})
        self.assertTrue({"page-h1", "heading-order", "empty-heading"} <= r)

    def test_viewport_zoom_block(self):
        head = '<meta name="viewport" content="width=device-width, maximum-scale=1">'
        self.assertIn("viewport-zoom", rules_found({"i.html": page("x", head)}, "fail"))

    def test_bypass_needs_main_or_skip(self):
        html = '<!DOCTYPE html><html lang="en"><head><title>t</title></head><body><nav><a href="/a">A</a></nav><div>x</div></body></html>'
        self.assertIn("bypass-blocks", rules_found({"i.html": html}, "fail"))
        tiny = '<!DOCTYPE html><html lang="en"><head><title>t</title></head><body><p>Just a note.</p></body></html>'
        self.assertNotIn("bypass-blocks", rules_found({"i.html": tiny}))

    def test_aria_problems(self):
        r = rules_found({"i.html": page('<a href="/" aria-hidden="true">x</a><div role="banner2"></div><div aria-labelledby="zz"></div>')}, "fail")
        self.assertTrue({"aria-hidden-focus", "aria-role", "aria-ref"} <= r)

    def test_media(self):
        r = rules_found({"i.html": page('<video src="v.mp4" autoplay></video>')})
        self.assertTrue({"media-alternative", "autoplay"} <= r)
        ok = page('<video src="v.mp4" controls><track kind="captions" src="c.vtt"></video>')
        self.assertNotIn("media-alternative", rules_found({"i.html": ok}))

    def test_paste_block(self):
        self.assertIn("auth-paste", rules_found({"i.html": page('<label>P<input type="password" onpaste="return false"></label>')}, "fail"))

    def test_click_without_keyboard(self):
        self.assertIn("click-no-keyboard", rules_found({"i.html": page('<div onclick="x()">go</div>')}, "fail"))

    def test_iframe_title(self):
        self.assertIn("frame-title", rules_found({"i.html": page('<iframe src="x"></iframe>')}, "fail"))

    def test_duplicate_id_only_when_referenced(self):
        self.assertNotIn("duplicate-id", rules_found({"i.html": page('<p id="a"></p><p id="a"></p>')}))
        self.assertIn("duplicate-id", rules_found({"i.html": page('<p id="a"></p><p id="a"></p><a href="#a">x</a>')}, "fail"))

    def test_client_rendered_warning(self):
        html = '<!DOCTYPE html><html lang="en"><head><title>t</title></head><body><div id="root"></div><script src="a.js"></script></body></html>'
        self.assertIn("client-rendered", rules_found({"i.html": html}, "review"))


class ContrastTests(unittest.TestCase):
    def contrast(self, css, body='<p class="t">Hello world</p>'):
        files = {"i.html": page(body, '<link rel="stylesheet" href="s.css">'), "s.css": css}
        res = scan(make_site(files))
        return [f for f in res.findings if f.rule.startswith("color-contrast") or f.rule == "contrast-unknown"]

    def test_low_contrast_fails(self):
        self.assertTrue(self.contrast(".t{color:#999;background:#fff}"))

    def test_good_contrast_passes(self):
        self.assertFalse(self.contrast(".t{color:#333;background:#fff}"))

    def test_large_text_threshold(self):
        css = ".t{color:#888;background:#fff;font-size:28px}"
        self.assertFalse(self.contrast(css))

    def test_bold_large(self):
        css = ".t{color:#888;background:#fff;font-size:19px;font-weight:700}"
        self.assertFalse(self.contrast(css))

    def test_inherited_background_from_ancestor(self):
        css = "main{background:#000} .t{color:#222}"
        self.assertTrue(self.contrast(css))

    def test_variable_resolution(self):
        css = ":root{--fg:#aaa} .t{color:var(--fg)}"
        self.assertTrue(self.contrast(css))

    def test_gradient_is_review_not_pass(self):
        css = "main{background:linear-gradient(#000,#fff)} .t{color:#777}"
        found = self.contrast(css)
        self.assertEqual({f.kind for f in found}, {"review"})

    def test_inline_style(self):
        self.assertTrue(self.contrast("", '<p style="color:#bbb">Hello world</p>'))

    def test_hidden_text_ignored(self):
        self.assertFalse(self.contrast(".t{color:#eee;display:none}"))


class StylesheetRuleTests(unittest.TestCase):
    def run_css(self, css):
        return rules_found({"i.html": page("<p>x</p>", '<link rel="stylesheet" href="s.css">'), "s.css": css}, None)

    def test_focus_outline_removed(self):
        self.assertIn("focus-visible", self.run_css("button:focus{outline:none}"))

    def test_focus_outline_replaced(self):
        self.assertNotIn("focus-visible", self.run_css("button:focus{outline:none;box-shadow:0 0 0 3px #05f}"))

    def test_global_reset_with_separate_focus_style(self):
        self.assertNotIn("focus-visible", self.run_css("*{outline:0} :focus-visible{outline:2px solid #05f}"))

    def test_sticky_without_scroll_padding(self):
        self.assertIn("focus-obscured", self.run_css("header{position:sticky;top:0}"))
        self.assertNotIn("focus-obscured", self.run_css("header{position:sticky} html{scroll-padding-top:4rem}"))

    def test_target_size(self):
        r = rules_found({"i.html": page('<button class="b">x</button>', '<link rel="stylesheet" href="s.css">'),
                         "s.css": ".b{width:16px;height:16px}"})
        self.assertIn("target-size", r)


class GroupingTests(unittest.TestCase):
    def test_template_issue_collapses_across_pages(self):
        files = {f"p{i}.html": page('<img src="a.png">') for i in range(5)}
        groups = [g for g in group(scan(make_site(files)).findings) if g["rule"] == "img-alt"]
        self.assertEqual(len(groups), 1)
        self.assertEqual(groups[0]["pages"], 5)


class ResolutionTests(unittest.TestCase):
    def test_root_relative_and_remote_stylesheets(self):
        files = {"blog/post.html": page("<p class='t'>Hi there</p>", '<link rel="stylesheet" href="/css/a.css"><link rel="stylesheet" href="https://cdn.example/x.css">'),
                 "css/a.css": ".t{color:#ccc}"}
        res = scan(make_site(files))
        self.assertIn("color-contrast", {f.rule for f in res.findings})
        self.assertEqual(res.remote_styles, ["https://cdn.example/x.css"])

    def test_missing_stylesheet_reported(self):
        res = scan(make_site({"i.html": page("x", '<link rel="stylesheet" href="nope.css">')}))
        self.assertEqual(len(res.missing_styles), 1)

    def test_path_traversal_stylesheet_not_read(self):
        outer = _tmp()
        with open(os.path.join(outer, "secret.css"), "w") as fh:
            fh.write("p{color:#fff}")
        site = os.path.join(outer, "site")
        os.makedirs(site)
        with open(os.path.join(site, "i.html"), "w") as fh:
            fh.write(page("<p>Hello world</p>", '<link rel="stylesheet" href="../secret.css">'))
        res = scan(site)
        self.assertEqual(res.stylesheets, [])


def run_cli(*argv):
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        code = cli.main(list(argv))
    return code, out.getvalue(), err.getvalue()


class CliTests(unittest.TestCase):
    def test_exit_codes(self):
        bad = make_site({"i.html": page('<img src="a.png">')})
        good = make_site({"index.html": GOOD_PAGE, "s.css": GOOD_CSS})
        self.assertEqual(run_cli("scan", bad)[0], 1)
        self.assertEqual(run_cli("scan", good)[0], 0)
        self.assertEqual(run_cli("scan", bad, "--fail-on", "never")[0], 0)
        self.assertEqual(run_cli("scan", "/nonexistent-dir")[0], 2)

    def test_json_output(self):
        bad = make_site({"i.html": page('<img src="a.png">')})
        code, out, _ = run_cli("scan", bad, "--format", "json")
        data = json.loads(out)
        self.assertEqual(data["summary"]["failures"], 1)
        self.assertTrue(data["manual_checks"])

    def test_init_refuses_overwrite(self):
        d = _tmp()
        path = os.path.join(d, "c.json")
        self.assertEqual(run_cli("init", "-o", path)[0], 0)
        self.assertEqual(run_cli("init", "-o", path)[0], 2)

    def test_statement_requires_config(self):
        site = make_site({"i.html": page("x")})
        self.assertEqual(run_cli("statement", site, "-c", "/nonexistent.json")[0], 2)

    def test_statement_warns_about_todos(self):
        site = make_site({"i.html": page("x")})
        cfgp = os.path.join(_tmp(), "c.json")
        run_cli("init", "-o", cfgp)
        code, out, err = run_cli("statement", site, "-c", cfgp)
        self.assertEqual(code, 0)
        self.assertIn("[TODO", out)
        self.assertIn("still marked [TODO]", err)


CFG = {"language": "en", "organisation": "Acme SRL", "website_url": "https://acme.example",
       "contact_email": "a11y@acme.example", "enforcement_authority": "Authority X (https://x.example)",
       "response_days": 10, "microenterprise": True, "date": "2026-10-28"}


class StatementTests(unittest.TestCase):
    def result(self, body):
        return scan(make_site({"i.html": page(body)}))

    def test_never_claims_full_conformance_by_default(self):
        text, todos = statement.render(self.result("<p>ok</p>"), CFG, "en", "md")
        self.assertEqual(todos, 0)
        self.assertIn("partially conformant", text)
        self.assertIn("not yet evaluated", text)
        self.assertNotIn("fully conformant", text)

    def test_full_only_with_manual_review_and_no_failures(self):
        cfg = dict(CFG, manual_review_done=True, manual_reviewer="Jane Doe")
        text, _ = statement.render(self.result("<p>ok</p>"), cfg, "en", "md")
        self.assertIn("fully conformant", text)
        text, _ = statement.render(self.result('<img src="x.png">'), cfg, "en", "md")
        self.assertNotIn("fully conformant", text)

    def test_limitations_listed_from_findings(self):
        text, _ = statement.render(self.result('<img src="x.png"><img src="y.png">'), CFG, "en", "md")
        self.assertIn("1.1.1 Non-text content", text)
        self.assertIn("2 place(s) on 1 page(s)", text)

    def test_microenterprise_note_toggle(self):
        r = self.result("<p>ok</p>")
        self.assertIn("microenterprise", statement.render(r, CFG, "en", "md")[0])
        self.assertNotIn("microenterprise", statement.render(r, dict(CFG, microenterprise=False), "en", "md")[0])

    def test_all_languages_render_with_same_structure(self):
        r = self.result('<img src="x.png">')
        counts = set()
        for lang in statement.LANGS:
            text, todos = statement.render(r, CFG, lang, "md")
            self.assertEqual(todos, 0)
            self.assertNotIn("{", text)
            counts.add(text.count("\n## "))
        self.assertEqual(len(counts), 1)
        self.assertIn("Declarație de accesibilitate", statement.render(r, CFG, "ro", "md")[0])

    def test_every_rule_wcag_has_a_translated_name(self):
        sample = {"1.1.1", "1.4.3", "2.4.7", "2.5.8", "3.3.8", "4.1.2", "2.4.11"}
        for lang in statement.LANGS:
            self.assertTrue(sample <= set(statement.SC_NAMES[lang]))

    def test_translations_are_complete(self):
        from eaa_audit import i18n
        for table in (i18n.T, i18n.SC_NAMES, i18n.NATIONAL_LAW, i18n.AUTHORITY_HINT):
            for lang in statement.LANGS:
                self.assertEqual(set(table[lang]) if isinstance(table[lang], dict) else True,
                                 set(table["en"]) if isinstance(table["en"], dict) else True, lang)
        for lang in statement.LANGS:
            self.assertEqual(len(i18n.MANUAL_LOCAL[lang]), len(i18n.MANUAL_LOCAL["en"]))

    def test_html_escaping(self):
        text, _ = statement.render(self.result("<p>x</p>"), dict(CFG, organisation="A <b>&Co"), "en", "html")
        self.assertIn("A &lt;b&gt;&amp;Co", text)
        self.assertNotIn("<b>", text)

    def test_all_sc_in_checks_are_named(self):
        import re
        with open(os.path.join(os.path.dirname(__file__), "..", "eaa_audit", "checks.py"), encoding="utf-8") as fh:
            src = fh.read()
        used = set(re.findall(r'self\.add\("[\w-]+", "(\d\.\d\.\d+)"', src)) | \
            set(re.findall(r'Finding\("[\w-]+", "(\d\.\d\.\d+)"', src))
        self.assertEqual(used - set(statement.SC_NAMES["en"]), set())


class ReviewPassTests(unittest.TestCase):
    def contrast_fail(self, css, body='<p class="t">Hello world</p>'):
        files = {"i.html": page(body, '<link rel="stylesheet" href="s.css">'), "s.css": css}
        return [f for f in scan(make_site(files)).findings if f.rule == "color-contrast"]

    def test_em_font_size_relative_to_parent(self):
        css = "main{font-size:10px} .t{color:#888;font-size:3em}"
        self.assertFalse(self.contrast_fail(css))
        css = "main{font-size:10px} .t{color:#888;font-size:1.2em}"
        self.assertTrue(self.contrast_fail(css))

    def test_font_shorthand(self):
        self.assertFalse(self.contrast_fail(".t{color:#888;font:bold 20px/1.4 Arial}"))
        self.assertTrue(self.contrast_fail(".t{color:#888;font:14px Arial}"))

    def test_default_link_colour_is_ua_blue(self):
        self.assertFalse(self.contrast_fail("body{color:#999}", '<a href="/x">Hello world</a>'))
        self.assertTrue(self.contrast_fail("body{color:#999}", '<p>Hello world</p>'))

    def test_unsupported_selector_is_reported(self):
        files = {"i.html": page("<p>x</p>", '<link rel="stylesheet" href="s.css">'),
                 "s.css": "p:nth-child(2n){color:#eee} a:hover{color:red}"}
        res = scan(make_site(files))
        self.assertEqual(len(res.unsupported_css), 1)
        self.assertEqual(report.summary(res)["ignored_css_rules"], 1)

    def test_link_underline_removed(self):
        files = {"i.html": page("<p>x</p>", '<link rel="stylesheet" href="s.css">'), "s.css": "a{text-decoration:none}"}
        self.assertIn("link-underline", {f.rule for f in scan(make_site(files)).findings})

    def test_duplicate_titles(self):
        files = {f"p{i}.html": page("<p>x</p>").replace("<title>t</title>", "<title>Same</title>") for i in range(3)}
        self.assertIn("duplicate-title", rules_found(files, "review"))

    def test_fix_advice_in_json(self):
        data = json.loads(report.to_json(scan(make_site({"i.html": page('<img src="a.png">')}))))
        self.assertIn("alt=", data["findings"][0]["fix"])

    def test_every_rule_has_advice(self):
        import re
        from eaa_audit import advice
        with open(os.path.join(os.path.dirname(__file__), "..", "eaa_audit", "checks.py"), encoding="utf-8") as fh:
            src = fh.read()
        with open(os.path.join(os.path.dirname(__file__), "..", "eaa_audit", "scanner.py"), encoding="utf-8") as fh:
            src += fh.read()
        rules = set(re.findall(r'(?:self\.add|Finding)\(\s*"([\w-]+)"', src)) - {"no-pages"}
        self.assertEqual(rules - set(advice.FIX), set())

    def test_onfocus_blur(self):
        self.assertIn("focus-blur", rules_found({"i.html": page('<a href="/x" onfocus="blur();">Go</a>')}, "fail"))

    def test_no_headings_on_long_page(self):
        self.assertIn("page-headings", rules_found({"i.html": page("<p>" + "word " * 120 + "</p>")}, "review"))

    def test_icon_background_with_fallback_colour_is_certain(self):
        css = "main{background:url(i.png) no-repeat 0 0 #fff} .t{color:#999}"
        files = {"i.html": page('<p class="t">Hello world</p>', '<link rel="stylesheet" href="s.css">'), "s.css": css}
        rules = {f.rule for f in scan(make_site(files)).findings}
        self.assertIn("color-contrast", rules)
        self.assertNotIn("contrast-unknown", rules)

    def test_uncertain_background_reported_once_per_layer(self):
        css = "main{background:linear-gradient(#000,#fff)}"
        files = {"i.html": page("<p>one one</p><p>two two</p><p>three</p>", '<link rel="stylesheet" href="s.css">'), "s.css": css}
        found = [f for f in scan(make_site(files)).findings if f.rule == "contrast-unknown"]
        self.assertEqual(len(found), 1)

    def test_single_file_scan(self):
        site = make_site({"i.html": page('<img src="a.png">'), "other.html": page("<p>fine</p>")})
        code, out, _ = run_cli("scan", os.path.join(site, "other.html"))
        self.assertEqual(code, 0)
        self.assertIn("Scanned 1 page", out)

    def test_baseline_roundtrip(self):
        site = make_site({"i.html": page('<img src="a.png">')})
        base = os.path.join(_tmp(), "base.json")
        self.assertEqual(run_cli("scan", site, "--write-baseline", base)[0], 0)
        self.assertEqual(run_cli("scan", site, "--baseline", base)[0], 0)
        with open(os.path.join(site, "new.html"), "w") as fh:
            fh.write(page('<button></button>'))
        self.assertEqual(run_cli("scan", site, "--baseline", base)[0], 1)

    def test_bad_baseline_file(self):
        site = make_site({"i.html": page("<p>x</p>")})
        self.assertEqual(run_cli("scan", site, "--baseline", "/nonexistent.json")[0], 2)

    def test_garbage_input_does_not_crash(self):
        import random
        rnd = random.Random(3)
        frags = ["<div", "</div>", "<img>", "{", "}", "a{color:", "<style>", "</style>", "var(--x", "@media(", "<svg>", "\x00", "&#x;", "calc(1px+", "<!--"]
        for _ in range(40):
            junk = "".join(rnd.choice(frags) + rnd.choice(["", " ", "x"]) for _ in range(rnd.randint(1, 60)))
            scan(make_site({"a.html": junk, "b.html": '<link rel=stylesheet href=s.css>' + junk, "s.css": junk}))

    def test_technologies_detected(self):
        files = {"i.html": page('<p role="note">x</p><script>1</script>', '<style>p{color:#000}</style>')}
        self.assertEqual(scan(make_site(files)).technologies, ["HTML", "CSS", "JavaScript", "WAI-ARIA"])
        self.assertEqual(scan(make_site({"i.html": page("<p>x</p>")})).technologies, ["HTML"])

    def test_statement_alternatives_technologies_review(self):
        r = scan(make_site({"i.html": page("<p>x</p>")}))
        for lang in statement.LANGS:
            cfg = dict(CFG, alternatives=["Phone support +40 1"], review_months=6)
            text = statement.render(r, cfg, lang, "md")[0]
            self.assertIn("Phone support +40 1", text)
            self.assertIn("HTML", text)
            self.assertIn("6", text)
            self.assertNotIn("{", text)

    def sheet(self, css, body='<p class="t">Hello world</p>', link=""):
        files = {"i.html": page(body, f'<link rel="stylesheet" href="s.css"{link}>'), "s.css": css}
        return scan(make_site(files))

    def test_dark_scheme_stylesheet_link_ignored(self):
        res = self.sheet(".t{color:#444;background:#555}", link=' media="(prefers-color-scheme: dark)"')
        self.assertEqual(res.stylesheets, [])
        self.assertNotIn("color-contrast", {f.rule for f in res.findings})

    def test_background_shorthand_resets_earlier_colour(self):
        res = self.sheet(".t{background-color:#000;color:#000} .t{background:transparent}")
        self.assertNotIn("color-contrast", {f.rule for f in res.findings})

    def test_visually_hidden_text_skipped(self):
        css = ".vh{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0,0,0,0);color:#eee}"
        res = self.sheet(css, '<p class="vh">Hidden label</p>')
        self.assertNotIn("color-contrast", {f.rule for f in res.findings})

    def test_same_colour_text_is_review_not_fail(self):
        res = self.sheet(".t{color:#fff;background:#fff}")
        kinds = {(f.rule, f.kind) for f in res.findings if f.rule.startswith("contrast") or f.rule == "color-contrast"}
        self.assertEqual(kinds, {("contrast-same", "review")})

    def test_text_indent_icon_button_skipped(self):
        res = self.sheet("button{text-indent:-5000px;overflow:hidden;background:#d2e2f1;color:#1d70b8}", "<button>Search</button>")
        self.assertNotIn("color-contrast", {f.rule for f in res.findings})

    def test_background_inherit_is_not_uncertain(self):
        res = self.sheet("main{background-color:inherit} .t{color:#333}")
        self.assertNotIn("contrast-unknown", {f.rule for f in res.findings})

    def test_focus_outline_patterns(self):
        rules = lambda css: {(f.rule, f.kind) for f in self.sheet(css).findings if f.rule == "focus-visible"}
        self.assertEqual(rules("a:focus:not(:focus-visible){outline:none}"), set())
        self.assertEqual(rules(".nav .btn:focus{outline:none} .btn:focus{box-shadow:0 0 0 3px #05f}"), set())
        self.assertEqual(rules("a:focus{outline:none}"), {("focus-visible", "fail")})
        self.assertEqual(rules("a:focus{outline:none} button:focus{box-shadow:0 0 0 2px #05f}"), {("focus-visible", "review")})

    def test_pseudo_element_rules_not_counted_as_unsupported(self):
        res = self.sheet(".t:after{color:#fff} .t::before{color:red}")
        self.assertEqual(res.unsupported_css, [])

    def test_empty_folder_exits_2(self):
        code, _, err = run_cli("scan", _tmp())
        self.assertEqual(code, 2)
        self.assertIn("No .html files", err)

    def test_ignore_rules(self):
        site = make_site({"i.html": page('<img src="a.png">')})
        self.assertEqual(run_cli("scan", site)[0], 1)
        self.assertEqual(run_cli("scan", site, "--ignore", "img-alt")[0], 0)

    def test_national_law_and_standard_in_statement(self):
        r = scan(make_site({"i.html": page("<p>x</p>")}))
        cfg = dict(CFG, national_law="Legea nr. 232/2022")
        text = statement.render(r, cfg, "ro", "md")[0]
        self.assertIn("Legea nr. 232/2022", text)
        self.assertIn("EN 301 549", text)
        self.assertIn("Legea nr. 232/2022", statement.starter_config("ro")["national_law"])


class DogfoodTests(unittest.TestCase):
    """Our own generated HTML must pass our own scanner."""

    def test_generated_pages_are_clean(self):
        site = make_site({"i.html": page('<img src="x.png">')})
        res = scan(site)
        d = _tmp()
        for lang in statement.LANGS:
            with open(os.path.join(d, f"s_{lang}.html"), "w", encoding="utf-8") as fh:
                fh.write(statement.render(res, CFG, lang, "html")[0])
        with open(os.path.join(d, "report.html"), "w", encoding="utf-8") as fh:
            fh.write(report.to_html(res))
        fails = [f for f in scan(d).findings if f.kind == "fail"]
        self.assertEqual(fails, [])


if __name__ == "__main__":
    unittest.main()
