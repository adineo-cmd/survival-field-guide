#!/usr/bin/env python3
"""Assemble the static multi-page site from shared template + content fragments.

Stdlib only. Run from repo root:  python3 tools/build.py
Inputs : content/pages/<id>.html   (hand-written page bodies, optional)
         content/<id>-extra.html   (distilled book fragments, optional)
         tools/books-inventory.tsv (library catalogue source)
Output : *.html at repo root.
"""
import os, sys, html, csv

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------- page spec
# id, file, num, kicker, title, desc, extra-fragment(s), scripts, wide-card
PAGES = [
    dict(id='priorities',   file='priorities.html',   num='01', kicker='Priorities',      title='Priorities & Mindset',   desc='The Rule of Threes, survival psychology, evasion and recovery — from the US Army survival manuals.', extras=['priorities-extra']),
    dict(id='shelter',      file='shelter.html',      num='02', kicker='Shelter',         title='Shelter',                desc='Debris huts, lean-tos, snow shelters and long-term camp structures, with build dimensions from the classic manuals.', extras=['shelter-extra']),
    dict(id='water',        file='water.html',        num='03', kicker='Water',           title='Water',                  desc='Finding, collecting and purifying water — solar stills, chemical dosing tables, boiling rules.', extras=['water-extra']),
    dict(id='fire',         file='fire.html',         num='04', kicker='Fire',            title='Fire',                   desc='Tinder-to-fuel craft, every fire lay, friction fire and all-weather techniques.', extras=['fire-extra']),
    dict(id='food',         file='food.html',         num='05', kicker='Food',            title='Food & Trapping',        desc='Snares and deadfalls, game care, preservation and camp cooking with real trail recipes.', extras=['food-extra']),
    dict(id='plants',       file='plants.html',       num='06', kicker='Plants',          title='Edible & Medicinal Plants', desc='Plant profiles with lookalike warnings, mushroom safety, and herbal preparation methods.', extras=['plants-edible','plants-medicinal']),
    dict(id='first-aid',    file='first-aid.html',    num='07', kicker='First Aid',       title='First Aid & Wilderness Medicine', desc='Bleeding control, wound closure, environmental casualties and improvised dental care.', extras=['firstaid-extra']),
    dict(id='navigate',     file='navigate.html',     num='08', kicker='Navigation',      title='Navigation & Signaling', desc='Map and compass craft, GPS-free methods, and the full rescue-signalling toolkit.', extras=['navigation-extra']),
    dict(id='knots',        file='knots.html',        num='09', kicker='Knots',           title='Knots, Lashings & Rope Work', desc='Every knot that matters, card by card — loops, hitches, lashings and fishing knots.', extras=['knots']),
    dict(id='cold-weather', file='cold-weather.html', num='10', kicker='Cold Weather',    title='Cold-Weather & Alpine Survival', desc='Heat loss, layering, snow shelters, ice safety and winter travel from the arctic manuals.', extras=['cold-weather']),
    dict(id='bushcraft',    file='bushcraft.html',    num='11', kicker='Bushcraft',       title='Bushcraft & Tools',      desc='Axecraft, cordage, containers, flintknapping, leather work and caching.', extras=['bushcraft']),
    dict(id='preparedness', file='preparedness.html', num='12', kicker='Preparedness',    title='Home & Urban Preparedness', desc='Nuclear, pandemic and disaster readiness — water math, shelter-in-place and go-bags.', extras=['preparedness']),
    dict(id='kit',          file='kit.html',          num='13', kicker='Gear',            title='The Kit',                desc='A 34-item packing checklist that saves your progress in the browser.', extras=[], scripts=['kit']),
    dict(id='library',      file='library.html',      num='14', kicker='The Library',     title='Source Library',         desc='The full catalogue of 150 survival books this guide was distilled from.', extras=[], scripts=['library']),
    dict(id='quiz',         file='quiz.html',         num='15', kicker='Field Exam',      title='Field Exam',             desc='Scenarios that test whether the manual stuck.', extras=[], scripts=['quiz']),
]

SCRIPTS = dict(
    kit   = '<script src="assets/kit.js"></script>',
    quiz  = '<script src="assets/quiz.js"></script>\n<script src="assets/faq.js"></script>',
    faq   = '<script src="assets/faq.js"></script>',
    library = '<script src="assets/library-data.js"></script>\n<script src="assets/library.js"></script>',
)

ICONS = """
<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
<symbol id="i-flame" viewBox="0 0 24 24"><path d="M12 3c1.8 2.7 3.2 4.5 3.2 6.7A3.2 3.2 0 0 1 12 12.8a3.2 3.2 0 0 1-3.2-3.1C7.3 11.3 6.2 13 6.2 15.2a5.8 5.8 0 0 0 11.6 0C17.8 10 15.2 6.6 12 3z"/></symbol>
<symbol id="i-drop" viewBox="0 0 24 24"><path d="M12 3.2s6 6.7 6 10.9a6 6 0 0 1-12 0c0-4.2 6-10.9 6-10.9z"/><path d="M9.5 13.5a2.6 2.6 0 0 0 2.5 3"/></symbol>
<symbol id="i-tent" viewBox="0 0 24 24"><path d="M12 4 2.5 20h19L12 4z"/><path d="M12 12.5 9.2 20M12 12.5l2.8 7.5"/></symbol>
<symbol id="i-leaf" viewBox="0 0 24 24"><path d="M5.5 18.5C5.5 9.5 12 4.5 20 4.5c0 8-5 14-14.5 14z"/><path d="M5.5 18.5c3-6 7-9 11-11"/></symbol>
<symbol id="i-med" viewBox="0 0 24 24"><rect x="3.5" y="7.5" width="17" height="12" rx="2.5"/><path d="M9 7.5V6a1.8 1.8 0 0 1 1.8-1.8h2.4A1.8 1.8 0 0 1 15 6v1.5M12 11v5M9.5 13.5h5"/></symbol>
<symbol id="i-compass" viewBox="0 0 24 24"><circle cx="12" cy="12" r="8.6"/><path d="m15.6 8.4-2.1 5.1-5.1 2.1 2.1-5.1z"/></symbol>
<symbol id="i-signal" viewBox="0 0 24 24"><circle cx="12" cy="10" r="2.2"/><path d="M12 12.2V21M8.2 6.4a5.4 5.4 0 0 0 0 7.2M15.8 6.4a5.4 5.4 0 0 1 0 7.2M5.4 3.6a9.4 9.4 0 0 0 0 12.8M18.6 3.6a9.4 9.4 0 0 1 0 12.8"/></symbol>
<symbol id="i-pack" viewBox="0 0 24 24"><path d="M8.5 7V5.5a3.5 3.5 0 0 1 7 0V7"/><rect x="5" y="7" width="14" height="13" rx="3"/><path d="M9.5 11.5h5v3.5h-5zM9 20v-2M15 20v-2"/></symbol>
<symbol id="i-alert" viewBox="0 0 24 24"><path d="M12 3.5 2.8 19.5h18.4L12 3.5z"/><path d="M12 10v4.5M12 17.2h.01"/></symbol>
<symbol id="i-menu" viewBox="0 0 24 24"><path d="M4 7h16M4 12h16M4 17h16"/></symbol>
<symbol id="i-up" viewBox="0 0 24 24"><path d="M12 19V5.5M6.5 11 12 5.5 17.5 11"/></symbol>
<symbol id="i-down" viewBox="0 0 24 24"><path d="M12 5.5V18M6.5 12.5 12 18l5.5-5.5"/></symbol>
<symbol id="i-star" viewBox="0 0 24 24"><path d="m12 3.5 2.5 5.3 5.7.7-4.2 3.9 1.1 5.6L12 16.2 6.9 19l1.1-5.6-4.2-3.9 5.7-.7L12 3.5z"/></symbol>
<symbol id="i-check" viewBox="0 0 24 24"><path d="m4.5 12.5 5 5.5L19.5 6.5"/></symbol>
<symbol id="i-sun" viewBox="0 0 24 24"><circle cx="12" cy="12" r="4.2"/><path d="M12 2.5v2.6M12 18.9v2.6M2.5 12h2.6M18.9 12h2.6M5.3 5.3l1.8 1.8M16.9 16.9l1.8 1.8M18.7 5.3l-1.8 1.8M7.1 16.9l-1.8 1.8"/></symbol>
<symbol id="i-shield" viewBox="0 0 24 24"><path d="M12 3 5 5.8v5.4c0 4.4 3 7.9 7 9.8 4-1.9 7-5.4 7-9.8V5.8L12 3z"/><path d="m9 11.6 2.2 2.2 3.8-4"/></symbol>
<symbol id="i-wind" viewBox="0 0 24 24"><path d="M3 8.5h9.5a2.7 2.7 0 1 0-2.7-2.7M3 13h14.5a2.7 2.7 0 1 1-2.7 2.7M3 17.5h6"/></symbol>
<symbol id="i-brain" viewBox="0 0 24 24"><path d="M9.5 4.5A3 3 0 0 0 6.6 8 3.2 3.2 0 0 0 4 11.2c0 1.3.7 2.4 1.8 3A3.1 3.1 0 0 0 9 19.5c1 0 1.9-.4 2.5-1.1V5.6a3 3 0 0 0-2-1.1zM14.5 4.5A3 3 0 0 1 17.4 8 3.2 3.2 0 0 1 20 11.2c0 1.3-.7 2.4-1.8 3A3.1 3.1 0 0 1 15 19.5c-1 0-1.9-.4-2.5-1.1V5.6a3 3 0 0 1 2-1.1z"/></symbol>
<symbol id="i-book" viewBox="0 0 24 24"><path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H20v15.5H6.5A2.5 2.5 0 0 0 4 21z"/><path d="M4 18.5A2.5 2.5 0 0 1 6.5 16H20"/></symbol>
</defs></svg>
"""

NAV_MAIN = [('priorities.html','Priorities'),('shelter.html','Shelter'),('water.html','Water'),
            ('fire.html','Fire'),('food.html','Food'),('plants.html','Plants'),
            ('first-aid.html','First Aid'),('navigate.html','Navigate')]
NAV_MORE = [('knots.html','Knots'),('cold-weather.html','Cold Weather'),('bushcraft.html','Bushcraft'),
            ('preparedness.html','Preparedness'),('kit.html','Kit'),('library.html','The Library')]

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — Survival Field Guide</title>
<meta name="description" content="{desc}">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'><text y='20' font-size='20'>🔥</text></svg>">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Saira+Stencil+One&family=Oswald:wght@400;500;600&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/style.css">
</head>
<body class="p-{id}">
{icons}
<div class="progress" id="progress"></div>

<nav class="nav" id="nav">
  <div class="callout-bar">In a real emergency, call your local emergency number first — <b>911 (US) / 112 (EU)</b><span class="callout-extra">. This guide is for preparedness, not a substitute for training</span>.</div>
  <div class="nav-inner">
    <a class="brand" href="index.html"><svg class="icon"><use href="#i-flame"/></svg>SURVIVAL<em>FIELD GUIDE</em></a>
    <button class="burger" id="burger" aria-label="Open menu" aria-expanded="false"><svg class="icon"><use href="#i-menu"/></svg></button>
    <div class="nav-links" id="navLinks">
      {navmain}
      <div class="nav-more">
        <button aria-haspopup="true">More <svg class="caret" viewBox="0 0 12 12"><path d="M2 4l4 4 4-4"/></svg></button>
        <div class="drop-menu">{navmore}<a href="quiz.html" class="hot">Field Exam</a></div>
      </div>
      <a href="quiz.html" class="hot">Exam</a>
    </div>
  </div>
</nav>

{body}

<footer class="foot">
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <a class="brand" href="index.html" style="margin-bottom:16px"><svg class="icon"><use href="#i-flame"/></svg>SURVIVAL<em>FIELD GUIDE</em></a>
        <p>A multi-page field manual distilled from 150 survival books — military manuals, classic bushcraft texts, plant guides and wilderness medical references.</p>
      </div>
      <div>
        <h4>Field chapters</h4>
        <a href="priorities.html">01 — Priorities &amp; mindset</a>
        <a href="shelter.html">02 — Shelter</a>
        <a href="water.html">03 — Water</a>
        <a href="fire.html">04 — Fire</a>
        <a href="food.html">05 — Food &amp; trapping</a>
        <a href="plants.html">06 — Plants</a>
        <a href="first-aid.html">07 — First aid</a>
        <a href="navigate.html">08 — Navigation &amp; signaling</a>
      </div>
      <div>
        <h4>&nbsp;</h4>
        <a href="knots.html">09 — Knots</a>
        <a href="cold-weather.html">10 — Cold weather</a>
        <a href="bushcraft.html">11 — Bushcraft</a>
        <a href="preparedness.html">12 — Preparedness</a>
        <a href="kit.html">13 — The kit</a>
        <a href="library.html">14 — Source library</a>
        <a href="quiz.html">15 — Field exam</a>
      </div>
    </div>
    <div class="disclaimer">
      <svg class="icon"><use href="#i-alert"/></svg>
      <div><b style="color:var(--bone)">Read this before you rely on it.</b> This guide distills reference books; it is not training, and plant or medicine entries can be wrong for your region or body. Learn hands-on with certified instructors, verify local laws, and in any genuine emergency call your local emergency number immediately: <b style="color:var(--bone)">911 (US) &nbsp;·&nbsp; 112 (EU) &nbsp;·&nbsp; 999 (UK) &nbsp;·&nbsp; 000 (AU)</b>.</div>
    </div>
    <div class="foot-big" aria-hidden="true">SURVIVE</div>
    <div class="foot-base">
      <span>SURVIVAL FIELD GUIDE — REV. 2026</span>
      <span>DISTILLED FROM 150 BOOKS</span>
      <span>© <span id="year"></span> · SHARE THE KNOWLEDGE</span>
    </div>
  </div>
</footer>

<button class="totop" id="totop" aria-label="Back to top"><svg class="icon"><use href="#i-up"/></svg></button>
<script src="assets/main.js"></script>
{scripts}
</body>
</html>
"""

def read(p):
    fp = os.path.join(ROOT, p)
    return open(fp, encoding='utf-8').read() if os.path.exists(fp) else None

def build_page(pg, prev, nxt):
    body = read(f"content/pages/{pg['id']}.html") or ''
    for ex in pg.get('extras', []):
        frag = read(f"content/{ex}.html")
        if frag:
            body += f"\n<!-- distilled from source books: {ex} -->\n" + frag
    pager = '<nav class="pager wrap" aria-label="Chapter navigation">'
    if prev:
        pager += f'<a class="prev" href="{prev["file"]}"><span class="dir">← PREVIOUS CHAPTER</span><span class="ttl">{html.escape(prev["title"])}</span></a>'
    else:
        pager += '<a class="prev" href="index.html"><span class="dir">← BACK TO</span><span class="ttl">Field Guide Home</span></a>'
    if nxt:
        pager += f'<a class="next" href="{nxt["file"]}"><span class="dir">NEXT CHAPTER →</span><span class="ttl">{html.escape(nxt["title"])}</span></a>'
    else:
        pager += '<a class="next" href="quiz.html"><span class="dir">FINISH WITH →</span><span class="ttl">The Field Exam</span></a>'
    pager += '</nav>'
    navmain = ''.join(f'<a href="{h}">{t}</a>' for h, t in NAV_MAIN)
    navmore = ''.join(f'<a href="{h}">{t}</a>' for h, t in NAV_MORE)
    out = TEMPLATE.format(
        id=pg['id'], title=pg['title'], desc=pg['desc'],
        icons=ICONS, navmain=navmain, navmore=navmore,
        body=body.rstrip() + '\n' + pager,
        scripts='\n'.join(SCRIPTS[s] for s in pg.get('scripts', [])),
    )
    with open(os.path.join(ROOT, pg['file']), 'w', encoding='utf-8') as f:
        f.write(out)
    return len(out)


def build_home():
    body = read("content/pages/_home.html") or ''
    navmain = ''.join(f'<a href="{h}">{t}</a>' for h, t in NAV_MAIN)
    navmore = ''.join(f'<a href="{h}">{t}</a>' for h, t in NAV_MORE)
    out = TEMPLATE.format(
        id='home', title='Survive Anything, Anywhere', 
        desc='A complete multi-page survival field guide distilled from 150 books: priorities, shelter, water, fire, food, plants, first aid, navigation, knots, cold weather, bushcraft and preparedness.',
        icons=ICONS, navmain=navmain, navmore=navmore, body=body.rstrip(),
        scripts='',
    )
    with open(os.path.join(ROOT, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(out)
    return len(out)

def main():
    total = build_home()
    print(f'{"index.html":22s} {total:>7,d} bytes')
    for i, pg in enumerate(PAGES):
        size = build_page(pg, PAGES[i-1] if i > 0 else None, PAGES[i+1] if i+1 < len(PAGES) else None)
        missing = [e for e in pg.get('extras', []) if not read(f"content/{e}.html")]
        flag = f'  (missing fragments: {", ".join(missing)})' if missing else ''
        print(f"{pg['file']:22s} {size:>7,d} bytes{flag}")
        total += size
    print(f'{"TOTAL":22s} {total:>7,d} bytes')

if __name__ == '__main__':
    main()
