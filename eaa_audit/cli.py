import argparse
import json
import os
import sys

from . import __version__
from . import report, statement
from .scanner import scan

CONFIG_NAME = "eaa-statement.json"


def build_parser():
    p = argparse.ArgumentParser(prog="eaa-audit", description="Scan a built static site for common WCAG 2.2 failures and draft the accessibility statement.")
    p.add_argument("--version", action="version", version=__version__)
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("scan", help="scan a folder of built HTML")
    s.add_argument("folder")
    s.add_argument("--format", choices=["text", "json", "html"], default="text")
    s.add_argument("-o", "--output", help="write report to a file instead of stdout")
    s.add_argument("--ignore", default="", metavar="RULES", help="comma-separated rule ids to skip, e.g. page-h1,target-size")
    s.add_argument("--fail-on", choices=["fail", "review", "never"], default="fail",
                   help="exit code 1 when this severity is found (default: fail)")

    i = sub.add_parser("init", help=f"write a starter {CONFIG_NAME}")
    i.add_argument("--lang", choices=sorted(statement.LANGS), default="en")
    i.add_argument("-o", "--output", default=CONFIG_NAME)

    st = sub.add_parser("statement", help="scan and draft the accessibility statement")
    st.add_argument("folder")
    st.add_argument("-c", "--config", default=CONFIG_NAME)
    st.add_argument("--lang", choices=sorted(statement.LANGS))
    st.add_argument("--format", choices=["md", "html"], default="html")
    st.add_argument("-o", "--output", help="output file (default: stdout)")
    return p


def _write(text, path):
    if path:
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text if text.endswith("\n") else text + "\n")
    else:
        print(text)


def main(argv=None):
    args = build_parser().parse_args(argv)
    if args.cmd == "init":
        if os.path.exists(args.output):
            print(f"{args.output} already exists; not overwriting.", file=sys.stderr)
            return 2
        _write(json.dumps(statement.starter_config(args.lang), indent=2, ensure_ascii=False), args.output)
        print(f"Wrote {args.output}. Fill in the fields, then run: eaa-audit statement <folder>", file=sys.stderr)
        return 0

    if not os.path.isdir(args.folder):
        print(f"Not a folder: {args.folder}", file=sys.stderr)
        return 2
    result = scan(args.folder)
    if not result.pages:
        print(f"No .html files found in {args.folder}. Point this at your built site folder (dist/, public/, _site/).", file=sys.stderr)
        return 2
    ignored = {r.strip() for r in getattr(args, "ignore", "").split(",") if r.strip()}
    result.findings = [f for f in result.findings if f.rule not in ignored]

    if args.cmd == "scan":
        if args.format == "json":
            out = report.to_json(result)
        elif args.format == "html":
            out = report.to_html(result)
        else:
            out = report.to_text(result, color=sys.stdout.isatty() and not args.output)
        _write(out, args.output)
        s = report.summary(result)
        bad = s["failures"] if args.fail_on == "fail" else s["failures"] + s["reviews"] if args.fail_on == "review" else 0
        return 1 if bad else 0

    try:
        with open(args.config, encoding="utf-8") as fh:
            cfg = json.load(fh)
    except FileNotFoundError:
        print(f"No {args.config}. Run 'eaa-audit init' first.", file=sys.stderr)
        return 2
    except json.JSONDecodeError as e:
        print(f"{args.config} is not valid JSON: {e}", file=sys.stderr)
        return 2
    lang = args.lang or cfg.get("language", "en")
    text, todos = statement.render(result, cfg, lang, args.format)
    _write(text, args.output)
    if todos:
        print(f"Warning: {todos} field(s) still marked [TODO]; fill them in {args.config} before publishing.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
