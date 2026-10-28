# EAA Site Auditor

Scans a **built static site folder** (`dist/`, `public/`, `_site/`) for common WCAG 2.2 failures and drafts the accessibility statement that the European Accessibility Act expects from many B2C sites. Pure Python standard library: no browser, no network, no install step beyond Python 3.9+.

RO: verifică accesibilitatea unui site (WCAG) și scrie declarația de accesibilitate (EN/RO/DE).

## Run

```bash
python3 -m eaa_audit scan ./dist                    # text report, exit 1 on failures
python3 -m eaa_audit scan ./dist --format html -o report.html
python3 -m eaa_audit scan ./dist --format json      # for CI
python3 -m eaa_audit init                           # writes eaa-statement.json
python3 -m eaa_audit statement ./dist --lang ro -o declaratie.html
```

Or `pip install .` and use the `eaa-audit` command. Tests: `python3 -m unittest discover -s tests`.

Publish the generated statement at a stable URL such as `/accessibility` and link it from the footer of every page.

`scan` also accepts a single `.html` file. `--fail-on fail|review|never` controls the exit code (default `fail`); `--ignore rule-a,rule-b` skips rules. Exit code 2 means a usage problem (e.g. no HTML files found). Every finding includes a one-line fix.

### In CI

Adopt it on an existing site without fixing everything first:

```bash
python3 -m eaa_audit scan ./dist --write-baseline a11y-baseline.json   # once, commit the file
python3 -m eaa_audit scan ./dist --baseline a11y-baseline.json          # fails only on new problems
```

## What it checks

| Finding | WCAG |
|---|---|
| Images/areas/SVG without text alternative, file-name alt text | 1.1.1 |
| Form fields without labels, label pointing nowhere, missing `autocomplete` | 3.3.2, 1.3.1, 1.3.5 |
| Links, buttons, frames, `role=button` without accessible name; vague link text | 2.4.4, 4.1.2 |
| Missing `lang`, `<title>`; no `<main>`/skip link; heading problems | 3.1.1, 2.4.2, 2.4.1, 2.4.6, 1.3.1 |
| Text contrast, computed from your own CSS files (selectors, inheritance, `var()`, alpha, large-text rule) | 1.4.3 |
| Zoom blocked in viewport meta, meta refresh, marquee, autoplay | 1.4.4, 2.2.1, 2.2.2, 1.4.2 |
| Focus outline removed with no replacement | 2.4.7 |
| Links with underline removed | 1.4.1 (review) |
| Same `<title>` on several pages | 2.4.2 (review) |
| Sticky/fixed elements with no `scroll-padding` | 2.4.11 (review) |
| Declared target size under 24 px | 2.5.8 (review) |
| Paste blocked on fields | 3.3.8 |
| Draggable items, `onclick` on non-interactive elements, positive tabindex, bad ARIA | 2.5.7, 2.1.1, 2.4.3, 4.1.2 |
| Video/audio without tracks | 1.2.1, 1.2.2 |

Results are `FAIL` (definite) or `REVIEW` (a human must decide). Identical findings repeated by a template across pages are grouped. Anything the tool cannot resolve (gradients, background images, remote CSS, client-side rendered pages) is reported as review, never as pass.

## Statement

`init` creates `eaa-statement.json`; fill it in, then run `statement`.

| Field | Meaning |
|---|---|
| `organisation`, `website_url`, `contact_email` | required; shown as `[TODO: …]` until set |
| `enforcement_authority` | the body users can complain to in your country and sector (required) |
| `national_law` | preset for `--lang ro` (Legea 232/2022) and `de` (BFSG) |
| `microenterprise` | adds the exemption note (fewer than 10 staff, up to EUR 2M) |
| `alternatives` | accessible alternatives for known problems (phone, e-mail, PDF …) |
| `measures` | what you do to keep the site accessible |
| `manual_review_done`, `manual_reviewer` | set after a human evaluation (keyboard, screen reader) |
| `response_days`, `review_months`, `date`, `contact_phone`, `contact_address` | optional |

The text contains the conformance status, known limitations from the scan (grouped by WCAG criterion), what only a human can verify, technologies detected (HTML, CSS, JavaScript, WAI-ARIA), contact, response time, enforcement body, review date and cadence. It names EN 301 549 (which requires WCAG 2.1 AA, the legal benchmark) and says the newer WCAG 2.2 criteria are also checked.

It says "partially conformant" unless you set `manual_review_done: true` **and** the scan has no failures. Unfilled fields are written as `[TODO: …]` and the command warns. The generated HTML passes this tool's own scan.

## Limits

- Speed: about 1 s per 1,600-element page with a deliberately heavy stylesheet (30 pages in 35 s); typical sites are much faster.

- Static analysis only. Axe-core's own docs say automation finds roughly 57% of WCAG issues; this finds fewer. Treat it as a first pass before manual and screen reader testing.
- CSS rules whose selectors it cannot evaluate and that set colours are counted in the report ("ignored CSS rules") so you know contrast may be incomplete.
- CSS support: tag/class/id/attribute selectors, descendant, child and sibling combinators, `:root`, `var()`. `:nth-child()`, `:is()`/`:where()`, other pseudo-classes beyond `:root`, `:first-child` and `:not()`, and width-conditional media queries are ignored.
- Statement templates are drafts, not legal advice. Whether your business is exempt, and which authority handles complaints, depends on your national law; check it.
