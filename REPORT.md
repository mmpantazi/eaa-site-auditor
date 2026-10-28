A zero-dependency Python CLI that scans a built static site folder for common WCAG 2.2 failures and drafts the EU accessibility statement (EN/RO/DE) from the results.

## What it does
- `scan`: ~35 static checks (alt text, labels, names, headings, landmarks, lang/title, viewport zoom, ARIA, media, focus outline removal, sticky-header obstruction, target size, paste blocking). Contrast is computed by resolving the site's own CSS (cascade, inheritance, `var()`, alpha, large-text rule). Output: text, JSON, accessible HTML. Exit code usable in CI.
- `init` / `statement`: drafts the statement from a small JSON config plus the scan. Status is "partially conformant" unless a human sets `manual_review_done` and there are no failures; unfilled fields show `[TODO]` and trigger a warning.
- Unresolvable cases (gradients, images, remote CSS, JS-rendered pages) become "review", never "pass".

## Run
`python3 -m eaa_audit scan ./dist`, `python3 -m eaa_audit init`, `python3 -m eaa_audit statement ./dist --lang ro -o out.html`. See README.md.

## Tested
59 `unittest` tests (`python3 -m unittest discover -s tests`), all passing: colour maths, CSS cascade, every rule positive and negative, grouping, stylesheet resolution including a path-traversal case, CLI exit codes, statement honesty rules, all three languages, HTML escaping, and a dogfood test that our generated HTML passes our own scanner. Also hand-probed with two small sample sites (found and fixed a media-query flattening false negative and a same-line undercount).

## Unfinished / caveats
- Reddit's archive returned 503 throughout, so research lacks Reddit threads (HN and YouTube used instead); see RESEARCH.md. Only 2 YouTube transcripts were read.
- Not run against real-world large sites (e.g. Hugo/Next exports); CSS support is deliberately limited (no sibling combinators, `:not()`, width-conditional media).
- Romanian national transposition law not verified; the RO template cites the Directive only. The microenterprise wording comes from vendor sources, not read from EUR-Lex (fetch failed). Statements are drafts, not legal advice.
- Rules are in English only; statement text is localized.
- The tool-created tests leave temp dirs behind.

## Next ideas
Sitemap-aware page weighting; `--baseline` file to ignore known issues in CI; GitHub Action; more languages (FR, IT, ES, NL, PL); verify statement fields against each country's authority; SARIF output; dedupe by shared template fragment; optional axe-core/Playwright pass when a browser exists.
