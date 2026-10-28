"""Draft the accessibility statement from scan results and a small config file."""

import datetime
import re
from html import escape

from .report import MANUAL_ONLY, summary
from .scanner import group

TODO = "[TODO: {}]"

SC_NAMES = {
    "en": {
        "1.1.1": "Non-text content (images without text alternatives)",
        "1.2.1": "Audio-only and video-only content",
        "1.2.2": "Captions for video",
        "1.3.1": "Info and relationships (structure)",
        "1.3.5": "Identify input purpose",
        "1.4.1": "Use of colour (links distinguishable from text)",
        "1.4.2": "Audio control",
        "1.4.3": "Contrast (minimum)",
        "1.4.4": "Resize text",
        "2.1.1": "Keyboard access",
        "2.2.1": "Timing adjustable",
        "2.2.2": "Pause, stop, hide",
        "2.4.1": "Bypass blocks",
        "2.4.2": "Page titled",
        "2.4.3": "Focus order",
        "2.4.4": "Link purpose",
        "2.4.6": "Headings and labels",
        "2.4.7": "Focus visible",
        "2.4.11": "Focus not obscured (minimum)",
        "2.5.7": "Dragging movements",
        "2.5.8": "Target size (minimum)",
        "3.1.1": "Language of page",
        "3.3.2": "Labels or instructions",
        "3.3.8": "Accessible authentication (minimum)",
        "4.1.2": "Name, role, value",
    },
    "ro": {
        "1.1.1": "Conținut non-text (imagini fără alternativă text)",
        "1.2.1": "Conținut doar audio sau doar video",
        "1.2.2": "Subtitrări pentru video",
        "1.3.1": "Informații și relații (structură)",
        "1.3.5": "Identificarea scopului câmpurilor",
        "1.4.1": "Utilizarea culorii (linkuri distincte de text)",
        "1.4.2": "Controlul sunetului",
        "1.4.3": "Contrast (minim)",
        "1.4.4": "Redimensionarea textului",
        "2.1.1": "Acces de la tastatură",
        "2.2.1": "Timp ajustabil",
        "2.2.2": "Pauză, oprire, ascundere",
        "2.4.1": "Ocolirea blocurilor repetitive",
        "2.4.2": "Titlul paginii",
        "2.4.3": "Ordinea focalizării",
        "2.4.4": "Scopul linkurilor",
        "2.4.6": "Titluri și etichete",
        "2.4.7": "Focalizare vizibilă",
        "2.4.11": "Focalizare neacoperită (minim)",
        "2.5.7": "Mișcări de tragere",
        "2.5.8": "Dimensiunea țintei (minim)",
        "3.1.1": "Limba paginii",
        "3.3.2": "Etichete sau instrucțiuni",
        "3.3.8": "Autentificare accesibilă (minim)",
        "4.1.2": "Nume, rol, valoare",
    },
    "de": {
        "1.1.1": "Nicht-Text-Inhalt (Bilder ohne Textalternative)",
        "1.2.1": "Reine Audio- oder Videoinhalte",
        "1.2.2": "Untertitel für Videos",
        "1.3.1": "Info und Beziehungen (Struktur)",
        "1.3.5": "Zweck von Eingabefeldern bestimmen",
        "1.4.1": "Verwendung von Farbe (Links vom Text unterscheidbar)",
        "1.4.2": "Audiosteuerung",
        "1.4.3": "Kontrast (Minimum)",
        "1.4.4": "Textgröße ändern",
        "2.1.1": "Tastaturbedienung",
        "2.2.1": "Zeitvorgaben anpassbar",
        "2.2.2": "Pausieren, beenden, ausblenden",
        "2.4.1": "Blöcke umgehen",
        "2.4.2": "Seitentitel",
        "2.4.3": "Fokusreihenfolge",
        "2.4.4": "Linkzweck",
        "2.4.6": "Überschriften und Beschriftungen",
        "2.4.7": "Sichtbarer Fokus",
        "2.4.11": "Fokus nicht verdeckt (Minimum)",
        "2.5.7": "Ziehbewegungen",
        "2.5.8": "Zielgröße (Minimum)",
        "3.1.1": "Sprache der Seite",
        "3.3.2": "Beschriftungen oder Anweisungen",
        "3.3.8": "Barrierefreie Authentifizierung (Minimum)",
        "4.1.2": "Name, Rolle, Wert",
    },
}

T = {
    "en": {
        "title": "Accessibility statement for {org}",
        "intro": "{org} is committed to making {site} accessible to people with disabilities, in line with the European Accessibility Act (Directive (EU) 2019/882) and the standard EN 301 549, which refers to the Web Content Accessibility Guidelines (WCAG).",
        "law": "National law: {law}.",
        "h_status": "Conformance status",
        "status_partial": "{site} is partially conformant with EN 301 549 (which requires WCAG 2.1 level AA). We also check the newer WCAG 2.2 criteria. Partially conformant means that some parts of the content do not fully meet the standard.",
        "status_full": "{site} is fully conformant with EN 301 549 (WCAG 2.1 level AA) and the WCAG 2.2 level AA criteria we checked, based on the evaluation described below.",
        "h_limits": "Known limitations",
        "limits_none": "The automated check found no failures. This does not prove that the site has no barriers.",
        "limits_intro": "The following content does not yet meet the requirements:",
        "limit_line": "{sc} {name}: {n} place(s) on {pages} page(s)",
        "review_intro": "These points were flagged for human review and may also be barriers:",
        "manual_intro": "These aspects cannot be verified by an automated tool and are {state}:",
        "manual_done": "covered by our manual evaluation",
        "manual_todo": "not yet evaluated",
        "h_micro": "Exemption",
        "micro": "{org} is a microenterprise within the meaning of Directive (EU) 2019/882 (fewer than 10 employees and annual turnover or balance sheet total of at most EUR 2 million). Service-related accessibility requirements do not legally apply to it; we publish this statement voluntarily and work to improve accessibility gradually.",
        "h_measures": "Measures to support accessibility",
        "measures_default": "We check pages with an automated tool before release.",
        "h_feedback": "Feedback and contact",
        "feedback": "If you cannot use part of this website, contact us and describe the problem and the page. We will reply within {days} days.",
        "contact_email": "E-mail: {v}",
        "contact_phone": "Phone: {v}",
        "contact_addr": "Address: {v}",
        "h_enforce": "Enforcement procedure",
        "enforce": "If you are not satisfied with our reply, you can complain to the competent authority: {auth}.",
        "h_prep": "Preparation of this statement",
        "prep": "This statement was prepared on {date}. Method: automated scan of {pages} page(s) with EAA Site Auditor{manual}.",
        "prep_manual": " and manual evaluation ({who})",
    },
    "ro": {
        "title": "Declarație de accesibilitate pentru {org}",
        "intro": "{org} se angajează să facă {site} accesibil persoanelor cu dizabilități, în conformitate cu Actul european privind accesibilitatea (Directiva (UE) 2019/882) și cu standardul EN 301 549, care face trimitere la Ghidul pentru accesibilitatea conținutului web (WCAG).",
        "law": "Legislația națională: {law}.",
        "h_status": "Starea de conformitate",
        "status_partial": "{site} este parțial conform cu EN 301 549 (care cere WCAG 2.1 nivel AA). Verificăm și criteriile mai noi din WCAG 2.2. Parțial conform înseamnă că unele părți ale conținutului nu respectă pe deplin standardul.",
        "status_full": "{site} este pe deplin conform cu EN 301 549 (WCAG 2.1 nivel AA) și cu criteriile WCAG 2.2 nivel AA verificate, pe baza evaluării descrise mai jos.",
        "h_limits": "Limitări cunoscute",
        "limits_none": "Verificarea automată nu a găsit erori. Acest lucru nu dovedește că site-ul nu are bariere.",
        "limits_intro": "Următorul conținut nu respectă încă cerințele:",
        "limit_line": "{sc} {name}: {n} locuri pe {pages} pagini",
        "review_intro": "Aceste puncte au fost semnalate pentru verificare manuală și pot constitui bariere:",
        "manual_intro": "Aceste aspecte nu pot fi verificate de un instrument automat și sunt {state}:",
        "manual_done": "acoperite de evaluarea noastră manuală",
        "manual_todo": "încă neevaluate",
        "h_micro": "Derogare",
        "micro": "{org} este o microîntreprindere în sensul Directivei (UE) 2019/882 (mai puțin de 10 angajați și cifră de afaceri anuală sau total bilanț de maximum 2 milioane EUR). Cerințele de accesibilitate pentru servicii nu i se aplică legal; publicăm această declarație voluntar și îmbunătățim accesibilitatea treptat.",
        "h_measures": "Măsuri pentru sprijinirea accesibilității",
        "measures_default": "Verificăm paginile cu un instrument automat înainte de publicare.",
        "h_feedback": "Feedback și contact",
        "feedback": "Dacă nu puteți utiliza o parte a acestui site, contactați-ne și descrieți problema și pagina. Vă vom răspunde în {days} zile.",
        "contact_email": "E-mail: {v}",
        "contact_phone": "Telefon: {v}",
        "contact_addr": "Adresă: {v}",
        "h_enforce": "Procedura de aplicare",
        "enforce": "Dacă nu sunteți mulțumit de răspunsul nostru, puteți depune o plângere la autoritatea competentă: {auth}.",
        "h_prep": "Elaborarea acestei declarații",
        "prep": "Declarația a fost elaborată la {date}. Metodă: scanare automată a {pages} pagini cu EAA Site Auditor{manual}.",
        "prep_manual": " și evaluare manuală ({who})",
    },
    "de": {
        "title": "Erklärung zur Barrierefreiheit für {org}",
        "intro": "{org} bemüht sich, {site} für Menschen mit Behinderungen zugänglich zu machen, gemäß dem Europäischen Barrierefreiheitsgesetz (Richtlinie (EU) 2019/882) und der Norm EN 301 549, die auf die Web Content Accessibility Guidelines (WCAG) verweist.",
        "law": "Nationales Recht: {law}.",
        "h_status": "Stand der Vereinbarkeit",
        "status_partial": "{site} ist teilweise mit EN 301 549 (die WCAG 2.1 Stufe AA verlangt) vereinbar. Wir prüfen zusätzlich die neueren Kriterien von WCAG 2.2. Teilweise vereinbar bedeutet, dass einige Inhalte die Norm nicht vollständig erfüllen.",
        "status_full": "{site} ist auf Grundlage der unten beschriebenen Bewertung vollständig mit EN 301 549 (WCAG 2.1 Stufe AA) und den geprüften WCAG-2.2-Kriterien Stufe AA vereinbar.",
        "h_limits": "Bekannte Einschränkungen",
        "limits_none": "Die automatische Prüfung hat keine Fehler gefunden. Das beweist nicht, dass die Website barrierefrei ist.",
        "limits_intro": "Die folgenden Inhalte erfüllen die Anforderungen noch nicht:",
        "limit_line": "{sc} {name}: {n} Stelle(n) auf {pages} Seite(n)",
        "review_intro": "Diese Punkte wurden zur manuellen Prüfung markiert und können ebenfalls Barrieren sein:",
        "manual_intro": "Diese Aspekte kann ein automatisches Werkzeug nicht prüfen; sie sind {state}:",
        "manual_done": "durch unsere manuelle Bewertung abgedeckt",
        "manual_todo": "noch nicht bewertet",
        "h_micro": "Ausnahme",
        "micro": "{org} ist ein Kleinstunternehmen im Sinne der Richtlinie (EU) 2019/882 (weniger als 10 Beschäftigte und Jahresumsatz oder Bilanzsumme von höchstens 2 Mio. EUR). Die Barrierefreiheitsanforderungen für Dienstleistungen gelten rechtlich nicht für uns; wir veröffentlichen diese Erklärung freiwillig und verbessern die Barrierefreiheit schrittweise.",
        "h_measures": "Maßnahmen zur Unterstützung der Barrierefreiheit",
        "measures_default": "Wir prüfen Seiten vor der Veröffentlichung mit einem automatischen Werkzeug.",
        "h_feedback": "Rückmeldung und Kontakt",
        "feedback": "Wenn Sie einen Teil dieser Website nicht nutzen können, schreiben Sie uns und beschreiben Sie das Problem und die Seite. Wir antworten innerhalb von {days} Tagen.",
        "contact_email": "E-Mail: {v}",
        "contact_phone": "Telefon: {v}",
        "contact_addr": "Anschrift: {v}",
        "h_enforce": "Durchsetzungsverfahren",
        "enforce": "Wenn Sie mit unserer Antwort nicht zufrieden sind, können Sie sich an die zuständige Behörde wenden: {auth}.",
        "h_prep": "Erstellung dieser Erklärung",
        "prep": "Diese Erklärung wurde am {date} erstellt. Methode: automatische Prüfung von {pages} Seite(n) mit EAA Site Auditor{manual}.",
        "prep_manual": " und manuelle Bewertung ({who})",
    },
}
LANGS = set(T)

MANUAL_LOCAL = {
    "en": MANUAL_ONLY,
    "ro": [
        "Utilizarea tuturor funcțiilor doar de la tastatură (2.1.1, 2.1.2)",
        "Dacă textele alternative sunt corecte și utile (1.1.1)",
        "Calitatea subtitrărilor, descrierilor audio și transcrierilor (1.2.x)",
        "Ordinea logică de citire (1.3.2)",
        "Contrastul textului peste imagini și al stărilor interactive (1.4.3, 1.4.11)",
        "Reorganizarea conținutului la 320 px și zoom 400% (1.4.10, 1.4.12)",
        "Focalizare vizibilă și ordinea focalizării (2.4.3, 2.4.7, 2.4.11)",
        "Navigare și ajutor consecvente între pagini (3.2.3, 3.2.6)",
        "Identificarea și corectarea erorilor din formulare (3.3.1, 3.3.3)",
        "Utilizarea cu un cititor de ecran real (4.1.2, 4.1.3)",
    ],
    "de": [
        "Bedienung aller Funktionen nur mit der Tastatur (2.1.1, 2.1.2)",
        "Ob Alternativtexte zutreffend und hilfreich sind (1.1.1)",
        "Qualität von Untertiteln, Audiodeskription und Transkripten (1.2.x)",
        "Sinnvolle Lesereihenfolge (1.3.2)",
        "Kontrast von Text auf Bildern und bei Zuständen wie Hover (1.4.3, 1.4.11)",
        "Reflow bei 320 px und 400 % Zoom, Textabstände (1.4.10, 1.4.12)",
        "Sichtbarer Fokus und Fokusreihenfolge (2.4.3, 2.4.7, 2.4.11)",
        "Einheitliche Navigation und Hilfe über alle Seiten (3.2.3, 3.2.6)",
        "Fehlererkennung und Korrekturvorschläge in Formularen (3.3.1, 3.3.3)",
        "Nutzung mit einem echten Screenreader (4.1.2, 4.1.3)",
    ],
}


NATIONAL_LAW = {"en": "", "ro": "Legea nr. 232/2022", "de": "Barrierefreiheitsstärkungsgesetz (BFSG)"}
AUTHORITY_HINT = {
    "en": "national market surveillance / enforcement body and URL",
    "ro": "autoritatea competentă pentru sectorul dvs. (ANPC, Autoritatea pentru Digitalizarea României, ANCOM, CNA …) și URL",
    "de": "zuständige Marktüberwachungsbehörde und URL",
}


def starter_config(lang="en"):
    return {
        "language": lang,
        "organisation": TODO.format("legal name of the website owner"),
        "website_url": TODO.format("https://example.eu"),
        "contact_email": TODO.format("accessibility contact e-mail"),
        "contact_phone": "",
        "contact_address": "",
        "response_days": 14,
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
    blocks += [("h2", t["h_prep"]), ("p", t["prep"].format(date=today, pages=s["pages"], manual=manual))]
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
