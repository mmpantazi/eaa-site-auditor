# Research notes

Reddit's Arctic Shift archive returned HTTP 503 on all six searches attempted, so Reddit was not available. HN (Algolia) and YouTube were used instead. Community-complaint evidence is therefore thinner than the brief asked for.

## Sources and what I learned

1. [Pa11y README](https://github.com/pa11y/pa11y) – Runs HTML_CodeSniffer or axe-core inside headless Chrome (Puppeteer). Local files need absolute paths. Needs Node 22+ and a browser download. No statement generation. Setup weight is the main friction for a small shop.
2. [axe-core README](https://github.com/dequelabs/axe-core) – Finds "on average 57% of WCAG issues automatically". Has only "limited support for JSDOM"; `color-contrast` is known not to work there. So browser-free contrast checking is a real gap.
3. [be-a11y (GitHub)](https://github.com/be-lenka/be-a11y) – Closest competitor (Show HN, May 2025). Node static linter, 29 rules for WCAG 2.1, folder/file/URL, JSON/HTML report, GitHub Action. Contrast covers inline styles only, does not resolve CSS files. No statement generator. WCAG 2.1, not 2.2.
4. [Show HN thread for be-a11y](https://news.ycombinator.com/item?id=44119516) – 6 points, two supportive comments: people want a "simple lightweight quick check" tool.
5. [AccessLint monorepo](https://github.com/accesslint/accesslint) – Core engine, CLI, Jest/Playwright matchers, MCP server. Developer tooling, no statement drafting, no EAA framing.
6. [access-sniff / HTML_CodeSniffer search result](https://github.com/silktide/HTML_CodeSniffer) – HTMLCS can run in jsdom, WCAG 2.0 only. Library, not a product for agencies.
7. [HN search "European Accessibility Act"](https://hn.algolia.com/api/v1/search?query=European%20Accessibility%20Act&tags=story) – Only ~13 stories, low engagement; the topic is under-served by dev tooling.
8. [W3C: What's New in WCAG 2.2](https://www.w3.org/WAI/standards-guidelines/wcag/new-in-22/) – Nine new criteria. AA ones: 2.4.11 Focus Not Obscured (Min), 2.5.7 Dragging, 2.5.8 Target Size (Min), 3.3.8 Accessible Authentication (Min); A: 3.2.6, 3.3.7. 4.1.1 Parsing is obsolete in 2.2.
9. [Deque WCAG 2.2 / TetraLogical / Eye-Able summaries](https://dequeuniversity.com/resources/wcag-2.2) – Target size and "fully hidden focus" can be partly tested; partial obscuring and focus-indicator adequacy need manual review. Old drafts (Focus Appearance AA) circulate and are wrong; final has it at AAA.
10. [W3C WAI accessibility statements](https://www.w3.org/WAI/planning/statements/) – Required: commitment, standard applied, contact. Advisable: known limitations, measures, technical prerequisites, tested environments, legal references. Plain language.
11. [Iubenda EAA statement guide](https://www.iubenda.com/en/help/181644-european-accessibility-act-eaa-accessibility-statement-guide-template) – EAA Annex V content: service description, how it operates, how Annex I requirements are met, monitoring. Known limitations/feedback are best practice rather than Annex V text.
12. [Stripo public statement](https://stripo.email/accessibility-statement/) and [eBay seller guide](https://www.ebay.ca/sellercentre/resources/european-accessibility-act) – Microenterprise (<10 staff and ≤€2M turnover/balance sheet) exemption for services (Directive 2019/882 Art. 4(5)); real statements declare it. Vendor sources, not legal text.
13. [MHC Ireland on statements](https://www.mhc.ie/latest/insights/european-accessibility-act-accessibility-statements) and [CMS summary](https://cms.law/en/cze/legal-updates/european-accessibility-act-what-does-this-mean-for-your-organisation) – EAA does not prescribe a statement format; public-sector model is Implementing Decision (EU) 2018/1523; EN 301 549 compliance is the presumption of conformity.
14. [TestParty template](https://testparty.ai/blog/eaa-accessibility-statement-required-fields-templates) and [Kolonell template](https://kolonell.com/en/blog/accessibility-statement-multi-year-plan-template-company-eaa-2026) – Typical fields: scope, standard, conformance status, limitations, feedback channel, response time, review date, plan. Response times/quarterly review are vendor practice, not law.
15. [YouTube: Louella Creemers, "What the new EAA means for web developers" (Vue.js Amsterdam)](https://youtu.be/fH2P9EjojNY) – Developers worry about fines; key points: B2C only, microenterprise exception, WCAG AA. Speaker also claims WCAG 2.1 is the one to follow (EN 301 549 v3.2.1 references 2.1; 2.2 is the safe superset).
16. [YouTube: Bet Hannon, EAA compliance (Equalize Digital meetup)](https://youtu.be/BEqFq8Vikp4) – EAA is a directive; each member state has its own transposing law and market-surveillance authority, so requirements differ by country. Enforcement began 28 June 2025; compliance includes paperwork beyond code.
17. [Pa11y/Lighthouse comparison results](https://www.ramotion.com/blog/practical-accessibility-testing-with-pa11y-and-axe-core/) – Typical advice: Pa11y for site-wide regression, Lighthouse per page; all need a browser.
18. Romanian transposition search (no Romanian law found in results; only Moldova/Spain) – I could not confirm the Romanian text, so the Romanian statement template cites the Directive, not a national law number.

## Gap and angle

Existing tools either need a headless browser (Pa11y, axe, Lighthouse) or are static linters that only read inline styles and target WCAG 2.1 (be-a11y). None produces the statement the EAA ecosystem actually asks for, and none speaks to a small agency delivering a built `dist/` folder to a client.

Angle for this project:
1. Zero-dependency (Python stdlib), works on a built folder offline, no browser.
2. Contrast computed by resolving the site's own CSS files (tag/class/id/descendant selectors, `var()`, inherited colours); anything it cannot resolve is reported as "needs manual check", never as pass.
3. WCAG 2.2 items checked statically where honest (2.4.7/2.4.11 outline removal, 2.5.8 declared target sizes, 3.3.8 password paste blocking).
4. Drafts the accessibility statement (EN/RO/DE) from the scan: conformance status and known limitations are generated from actual findings plus an explicit list of what automation cannot verify. Placeholders for fields only the client knows are marked and the tool warns.
5. Honest framing: automated tools find a minority of issues (axe: ~57%), so the statement says "partially conformant, automated check only" and never claims full conformance.
