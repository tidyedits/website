"""Builds the service, town and guide pages plus sitemap.xml.

Run from the repo root:  python3 _build/build.py
Shared styles come from _build/base.css (copied from index.html) + PAGE_CSS below.
"""
import json
import os
import sys
from datetime import date
from html import escape

sys.path.insert(0, os.path.dirname(__file__))
from content import ANSWERS, AREAS, GUIDES, SERVICES  # noqa: E402
from plan import PLAN_CSS, plan_body  # noqa: E402

SITE = "https://tidyedits.com"
PHONE, TEL = "857-753-5593", "tel:+18577535593"
TODAY = date.today().isoformat()
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SVC = {s["slug"]: s for s in SERVICES}
AREA = {a["slug"]: a for a in AREAS}

PAGE_CSS = """
/* Inner pages */
.crumbs { font-size: var(--step--1); color: var(--muted); padding-top: var(--space-3); }
.crumbs a { color: var(--muted); }
.hero { padding-block: var(--space-4) var(--section); display: grid; gap: var(--space-3); justify-items: start; }
.hero h1 { font-size: var(--step-4); max-width: 15em; }
.hero .lede { font-size: var(--step-1); line-height: 1.5; color: var(--muted); max-width: 40rem; }
.ctas { display: flex; flex-wrap: wrap; gap: 12px; }
.split { display: grid; grid-template-columns: 0.9fr 1.6fr; gap: var(--space-4); padding-block: var(--space-4); border-top: 1px solid var(--ink); }
.split + .split { border-top-color: var(--line); }
.split h2 { font-size: var(--step-2); line-height: 1.1; }
.split p { color: var(--muted); max-width: 62ch; }
.ticks { list-style: none; margin: 0; padding: 0; display: grid; grid-template-columns: 1fr 1fr; gap: 12px var(--space-4); }
.ticks li { padding-left: 26px; position: relative; }
.ticks li::before { content: ""; position: absolute; left: 2px; top: .55em; width: 12px; height: 6px; border-left: 2px solid var(--tan); border-bottom: 2px solid var(--tan); transform: rotate(-45deg); }
.links { list-style: none; margin: 0; padding: 0; columns: 2; column-gap: var(--space-4); }
.links li { padding-block: 10px; border-bottom: 1px solid var(--line); break-inside: avoid; }
.links a { font-family: var(--display); font-size: 1.2rem; color: var(--ink); text-decoration: none; }
.links a:hover { color: var(--tan); }
.note { color: var(--muted); }
.cta-band { display: grid; gap: var(--space-2); justify-items: start; }
.cta-band h2 { font-size: var(--step-3); }
.foot-links { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: var(--space-3); width: 100%; margin-bottom: var(--space-4); }
.foot-links h3 { font-size: var(--step--1); text-transform: uppercase; letter-spacing: .08em; color: var(--ink); margin-bottom: 8px; }
.foot-links ul { list-style: none; margin: 0; padding: 0; display: grid; gap: 6px; }
.foot-links a { color: var(--muted); text-decoration: none; }
.foot-links a:hover { color: var(--ink); }
@media (max-width: 860px) { .split { grid-template-columns: 1fr; gap: var(--space-2); } }
@media (max-width: 560px) { .ticks, .links { grid-template-columns: 1fr; columns: 1; } .foot-links { grid-template-columns: 1fr 1fr; } }
.answer p { font-size: var(--step-1); line-height: 1.5; color: var(--ink); max-width: 60ch; }
"""


def ld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, indent=1) + "</script>"


def crumbs_ld(trail):
    return {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + u}
            for i, (n, u) in enumerate(trail)
        ],
    }


def faq_ld(faq):
    return {
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in faq
        ],
    }


def footer_links():
    col = lambda title, items: (
        f"<div><h3>{title}</h3><ul>"
        + "".join(f'<li><a href="{u}">{escape(n)}</a></li>' for n, u in items)
        + "</ul></div>"
    )
    return (
        '<nav class="foot-links" aria-label="Site">'
        + col("Services", [(s["name"], f"/services/{s['slug']}/") for s in SERVICES])
        + col("Areas", [(a["name"], f"/areas/{a['slug']}/") for a in AREAS])
        + col("Guides", [(g["h1"].split(":")[0], f"/guides/{g['slug']}/") for g in GUIDES])
        + "</nav>"
    )


def page(path, title, desc, body, trail, extra_ld=()):
    url = SITE + path
    graph = [crumbs_ld(trail), *extra_ld]
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{escape(title)}</title>
<meta name="description" content="{escape(desc)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Tidy Edits Cleaning Company">
<meta property="og:title" content="{escape(title)}">
<meta property="og:description" content="{escape(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/logo.png">
<meta name="theme-color" content="#faf6f0" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#1a1511" media="(prefers-color-scheme: dark)">
<link rel="icon" href="/logo.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,opsz,wght@0,6..96,400..700;1,6..96,400..600&family=Figtree:wght@400;500;600&display=swap">
<link rel="stylesheet" href="/assets/site.css">
{ld({"@context": "https://schema.org", "@graph": graph})}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site">
  <div class="wrap nav">
    <a class="logo" href="/"><img src="/logo.png" alt="Tidy Edits" width="82" height="60"></a>
    <nav class="nav-links" aria-label="Main">
      <a href="/services/">Services</a>
      <a href="/areas/">Service area</a>
      <a href="/guides/">Guides</a>
      <a href="/plan/">Plan your clean</a>
      <a href="/#faq">Questions</a>
    </nav>
    <a class="nav-phone" href="{TEL}">{PHONE}</a>
    <a class="btn btn-solid btn-sm" href="/#quote">Free quote</a>
  </div>
</header>
<main id="main">
  <div class="wrap">
    <p class="crumbs">{" / ".join(f'<a href="{u}">{escape(n)}</a>' for n, u in trail[:-1])} / {escape(trail[-1][0])}</p>
{body}
  </div>
  <section class="section oat">
    <div class="wrap cta-band">
      <h2>Get a quote for your place</h2>
      <p class="note">We do all types of cleaning jobs, small or large, one-time or recurring. Tell us about the property and we'll tailor the quote.</p>
      <div class="ctas"><a class="btn btn-solid" href="/#quote">Request a free quote</a><a class="btn btn-line" href="/plan/">Plan your clean</a><a class="btn btn-line" href="{TEL}">Call or text {PHONE}</a></div>
    </div>
  </section>
</main>
<footer class="site">
  <div class="wrap foot">
    {footer_links()}
    <div><img src="/logo.png" alt="" width="99" height="72" loading="lazy"><strong translate="no">Tidy Edits Cleaning Company</strong><br>Residential and commercial cleaning, Greater Boston</div>
    <div><a href="{TEL}">{PHONE}</a> · <a href="mailto:info@tidyedits.com">info@tidyedits.com</a><br>Serving Boston and Greater Boston, MA</div>
  </div>
</footer>
<div class="callbar">
  <a class="btn btn-line" href="{TEL}">Call</a>
  <a class="btn btn-solid" href="/#quote">Free quote</a>
</div>
</body>
</html>
"""


def ticks(items):
    return '<ul class="ticks">' + "".join(f"<li>{escape(i)}</li>" for i in items) + "</ul>"


def link_list(items):
    return '<ul class="links">' + "".join(f'<li><a href="{u}">{escape(n)}</a></li>' for n, u in items) + "</ul>"


def faq_html(faq):
    return '<div class="faq">' + "".join(
        f"<details><summary>{escape(q)}</summary><p>{escape(a)}</p></details>" for q, a in faq
    ) + "</div>"


def split(h, inner, cls=""):
    return f'    <section class="split{(" " + cls) if cls else ""}"><h2>{h}</h2><div>{inner}</div></section>\n'


def hero(h1, lede):
    return (
        f'    <div class="hero"><h1>{escape(h1)}</h1><p class="lede">{escape(lede)}</p>'
        f'<div class="ctas"><a class="btn btn-solid" href="/#quote">Get a free quote</a>'
        f'<a class="btn btn-line" href="{TEL}">Call {PHONE}</a></div></div>\n'
    )


def service_ld(name, path, area_names):
    return {
        "@type": "Service",
        "name": name,
        "url": SITE + path,
        "provider": {"@id": SITE + "/#business"},
        "areaServed": [{"@type": "City", "name": f"{n}, MA"} for n in area_names],
    }


def write(path, html):
    out = os.path.join(ROOT, path.strip("/"), "index.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w") as f:
        f.write(html)
    return path


def build():
    with open(os.path.join(ROOT, "_build", "base.css")) as f:
        css = "/* Generated by _build/build.py from index.html styles. */\n" + f.read() + PAGE_CSS + PLAN_CSS
    with open(os.path.join(ROOT, "assets", "site.css"), "w") as f:
        f.write(css)

    town_names = [a["name"] for a in AREAS]
    paths = []
    home = ("Home", "/")

    for s in SERVICES:
        p = f"/services/{s['slug']}/"
        others = [(o["name"], f"/services/{o['slug']}/") for o in SERVICES if o is not s]
        q, ans = ANSWERS[s["slug"]]
        body = hero(s["h1"], s["lede"])
        body += split(escape(q), f"<p>{escape(ans)}</p>", "answer")
        body += split("What's included", ticks(s["included"]) + '<p class="note" style="margin-top:16px">Every clean is tailored to the property. Need something not listed? Ask. We do all types of cleaning jobs.</p>')
        body += split("Who it's for", f"<p>{escape(s['who'])}</p>")
        body += split("Around Greater Boston", f"<p>{escape(s['local'])}</p>" + link_list([(f"{s['name']} in {a['name']}", f"/areas/{a['slug']}/") for a in AREAS[:4]]))
        if s["guide"]:
            g = next(g for g in GUIDES if g["slug"] == s["guide"])
            body += split("Free checklist", f'<p><a href="/guides/{g["slug"]}/">{escape(g["h1"])}</a></p>')
        body += split("Questions", faq_html(s["faq"]))
        body += split("Other services", link_list(others))
        paths.append(write(p, page(p, s["title"], s["desc"], body,
                                   [home, ("Services", "/services/"), (s["name"], p)],
                                   [service_ld(s["name"], p, town_names), faq_ld([(q, ans)] + s["faq"])])))

    for a in AREAS:
        p = f"/areas/{a['slug']}/"
        n = a["name"]
        body = hero(f"House and office cleaning in {n}, MA", a["intro"])
        body += split(f"Cleaning in {n}", f"<p>{escape(a['angle'])}</p>")
        body += split(f"Services in {n}", link_list([(s["name"], f"/services/{s['slug']}/") for s in SERVICES])
                      + '<p class="note" style="margin-top:16px">These are examples. We do all types of cleaning jobs, from one room to a whole building.</p>')
        body += split("How it works", "<p>Tell us about the place by form, call or text. We send a quote tailored to its size and condition. Smaller jobs we handle ourselves, and we bring a full team for large homes and buildings. Then you walk through, and if something's missed, we make it right.</p>")
        body += split("Nearby", link_list([(f"Cleaning in {AREA[x]['name']}", f"/areas/{x}/") for x in a["nearby"]]))
        faq = [(f"Do you clean in {n}?", f"Yes. Tidy Edits cleans homes, rentals, listings, buildings and offices in {n} and across Greater Boston. Call {PHONE} or request a quote online."),
               ("Do you take small jobs?", "Yes. We handle small jobs ourselves and bring in a team for large ones.")]
        body += split("Questions", faq_html(faq))
        paths.append(write(p, page(p, a["title"], a["desc"], body,
                                   [home, ("Service area", "/areas/"), (n, p)],
                                   [service_ld(f"House cleaning in {n}", p, [n]), faq_ld(faq)])))

    for g in GUIDES:
        p = f"/guides/{g['slug']}/"
        s = SVC[g["service"]]
        body = f'    <article class="hero"><h1>{escape(g["h1"])}</h1><p class="lede">{escape(g["lede"])}</p></article>\n'
        for h, items in g["sections"]:
            body += split(escape(h), ticks(items))
        body += split("Pro tip", f"<p>{escape(g['tip'])}</p>")
        body += split("Rather we did it?", f'<p>Tidy Edits does this for clients across Greater Boston. See <a href="/services/{s["slug"]}/">{escape(s["name"].lower())}</a>, or call {PHONE}.</p>')
        art = {"@type": "Article", "headline": g["h1"], "description": g["desc"], "url": SITE + p,
               "datePublished": "2026-10-23", "dateModified": TODAY,
               "author": {"@id": SITE + "/#business"}, "publisher": {"@id": SITE + "/#business"},
               "image": SITE + "/logo.png"}
        paths.append(write(p, page(p, g["title"], g["desc"], body,
                                   [home, ("Guides", "/guides/"), (g["h1"].split(":")[0], p)], [art])))

    hubs = [
        ("/services/", "Cleaning Services in Greater Boston | Tidy Edits",
         "House, apartment, rental, Airbnb, listing prep, common area and office cleaning across Greater Boston. All types of cleaning jobs. 857-753-5593.",
         "Cleaning services", "We do all types of cleaning jobs, small or large. These are the ones people ask for most.", "Services",
         [(s["name"], f"/services/{s['slug']}/") for s in SERVICES]),
        ("/areas/", "Cleaning Service Area: Boston and Nearby Towns | Tidy Edits",
         "Tidy Edits cleans homes, rentals and offices in Boston, Dorchester, Cambridge, Somerville, Brookline, Quincy, Milton, Newton and nearby towns.",
         "Where we clean", "Boston and the towns around it. Don't see yours? Call us. We often travel for larger jobs.", "Service area",
         [(f"Cleaning in {a['name']}", f"/areas/{a['slug']}/") for a in AREAS]),
        ("/guides/", "Cleaning Checklists and Guides | Tidy Edits",
         "Free cleaning checklists from Tidy Edits: move-out, Airbnb turnover, deep cleaning and pre-sale listing prep.",
         "Cleaning checklists", "The same checklists we use on the job. Save them, print them, or let us do it.", "Guides",
         [(g["h1"], f"/guides/{g['slug']}/") for g in GUIDES]),
    ]
    for p, title, desc, h1, lede, crumb, items in hubs:
        body = hero(h1, lede) + split("Pages", link_list(items))
        paths.append(write(p, page(p, title, desc, body, [home, (crumb, p)])))

    p = "/plan/"
    paths.append(write(p, page(p, "Plan Your Clean: Free Cleaning Plan and Quote | Tidy Edits",
                               "Tap through a few questions and get a tailored cleaning plan for your home, rental or office in Greater Boston. Send it for a free quote.",
                               plan_body(SERVICES, GUIDES), [home, ("Plan your clean", p)])))

    urls = ["/"] + paths
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    sm += [f"  <url><loc>{SITE}{u}</loc><lastmod>{TODAY}</lastmod></url>" for u in urls]
    sm.append("</urlset>")
    with open(os.path.join(ROOT, "sitemap.xml"), "w") as f:
        f.write("\n".join(sm) + "\n")
    print(f"{len(paths)} pages + sitemap ({len(urls)} urls)")


if __name__ == "__main__":
    build()
