"""Build the Lumetra Impianti demo (fictional business). Run: python scripts/build_site.py.

All business facts and historical projects live in content/site.json.
No external generator, framework, CDN or backend is required.
"""
from html import escape as e
import json
import hashlib
import re
from pathlib import Path
from urllib.parse import urlencode

ROOT = Path(__file__).resolve().parent.parent
DATA = json.loads((ROOT / 'content/site.json').read_text(encoding='utf-8'))
MEDIA = json.loads((ROOT / 'content/media.json').read_text(encoding='utf-8'))
SERVICES, WORKS = DATA['comp'], DATA['works']
SMAP = {s['slug']: s for s in SERVICES}
WMAP = {w['slug']: w for w in WORKS}
URL = 'https://gxmich.github.io/lumetra-impianti-demo'
BASE_PATH = '/lumetra-impianti-demo/'
TEL = '+39 000 000 0000'
EMAIL = 'info@lumetra-impianti.example'
MAP = 'contatti.html#sede'
ARROW = '<svg class="ar" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 12h15m-5-5 5 5-5 5" fill="none" stroke="currentColor" stroke-width="1.6"/></svg>'
NAV = [('competenze.html', 'Impianti e servizi'), ('lavori.html', 'Lavori'), ('assistenza.html', 'Assistenza'), ('azienda.html', 'Azienda'), ('contatti.html', 'Contatti')]
PROFILES = ['Azienda o attività', 'Ente pubblico', 'Progettista o impresa edile', 'Privato o condominio']
COVER_FOCUS = {'passerella-torrente': '50% 55%'}
COVER_FOCUS_PHONE = {}
CARD_FOCUS = {}
# Home service previews must not repeat a photograph already shown on the home page.
SERVICE_PREVIEW = {'impianti-elettrici': 'interruttori'}


def contact(**params):
    """Prefilled requests land directly on the form."""
    return 'contatti.html' + ('?' + e(urlencode(params)) + '#richiesta' if params else '')


def button(label, href='contatti.html', style='blue', extra=''):
    return f'<a class="btn btn-{style}{extra}" href="{href}">{label}{ARROW}</a>'


def image(name, alt='', lazy=True, sizes='(max-width: 760px) 100vw, 55vw', css='', bleed=False, style=''):
    w, h = MEDIA[name]
    candidates = [f'img/{name}-{size}.webp {size}w' for size in (480, 640, 900, 1280) if size < w and (ROOT / 'img' / f'{name}-{size}.webp').exists()]
    candidates.append(f'img/{name}.webp {w}w')
    if not bleed:
        sizes = sizes.replace('100vw', 'calc(100vw - 44px)')
    srcset = f' srcset="{", ".join(candidates)}" sizes="{sizes}"'
    loading = ' loading="lazy"' if lazy else ' fetchpriority="high"'
    css_attr = f' class="{css}"' if css else ''
    style_attr = f' style="{style}"' if style else ''
    return f'<img src="img/{name}.webp" width="{w}" height="{h}" alt="{e(alt)}"{srcset}{loading} decoding="async"{css_attr}{style_attr}>'


def nav(active, mobile=False):
    links = [('index.html', 'Home')] + NAV if mobile else NAV
    return ''.join(f'<a href="{href}"' + (' aria-current="page"' if href == active else '') + f'>{label}</a>' for href, label in links)


def header(active):
    return f'''<a class="skip" href="#contenuto">Vai al contenuto</a>
<header class="hd" data-header>
  <div class="hd-util"><div class="wrap hd-util-in"><span>Impianti elettrici e tecnologici · Rocca Tessera, dal 1987</span><span class="hd-util-links"><a href="tel:+390000000000">{TEL}</a><a href="mailto:{EMAIL}">{EMAIL}</a></span></div></div>
  <div class="wrap hd-main">
    <a class="hd-logo" href="index.html" aria-label="Lumetra Impianti, home"><img src="img/logo-lumetra.svg" alt="Lumetra Impianti" width="520" height="165"></a>
    <nav class="hd-nav" aria-label="Navigazione principale">{nav(active)}</nav>
    {button('Parliamo del progetto', style='red', extra=' hd-cta')}
    <button class="hd-burger" type="button" data-menu-toggle aria-label="Apri il menu" aria-haspopup="dialog" aria-controls="menu" aria-expanded="false"><span class="burger-lines" aria-hidden="true"></span><span>Menu</span></button>
  </div>
</header>
<dialog class="menu" id="menu" aria-labelledby="menu-title">
  <div class="menu-top"><p id="menu-title">Lumetra Impianti</p><button class="menu-close" type="button" data-menu-close aria-label="Chiudi il menu">Chiudi <span aria-hidden="true">×</span></button></div>
  <nav class="menu-links" aria-label="Navigazione mobile">{nav(active, True)}</nav>
  <div class="menu-foot"><p>Impianti elettrici e tecnologici, dal progetto alla manutenzione.</p><a class="menu-phone" href="tel:+390000000000">{TEL}</a><a href="mailto:{EMAIL}">{EMAIL}</a>{button('Parliamo del progetto', style='red')}</div>
</dialog>'''


def footer(bar=None):
    """bar: (label, href) of the fixed phone action, contextual on service and assistance pages."""
    bar_label, bar_href = bar or ('Parliamo del progetto', 'contatti.html')
    services = ''.join(f'<li><a href="competenza-{s["slug"]}.html">{e(s["short"])}</a></li>' for s in SERVICES)
    return f'''<footer class="ft">
  <div class="wrap ft-grid">
    <div class="ft-brand"><a href="index.html" aria-label="Lumetra Impianti, home"><img src="img/logo-lumetra.svg" alt="Lumetra Impianti" width="520" height="165" loading="lazy"></a><p>Impianti elettrici e tecnologici,<br>dal progetto alla manutenzione.<br>A Rocca Tessera dal 1987.</p></div>
    <div><p class="ft-h">Impianti e servizi</p><ul>{services}<li><a href="assistenza.html">Assistenza e manutenzione</a></li></ul></div>
    <div><p class="ft-h">Azienda</p><ul><li><a href="lavori.html">Lavori realizzati</a></li><li><a href="azienda.html">Storia e organizzazione</a></li><li><a href="azienda.html#qualifiche">Qualificazioni</a></li><li><a href="azienda.html#referenze">Settori</a></li><li><a href="contatti.html">Contatti</a></li></ul></div>
    <div class="ft-contact"><p class="ft-h">Sede</p><address>Via delle Fornaci 8<br>Rocca Tessera (Piemonte)</address><a href="tel:+390000000000" class="ft-phone">{TEL}</a><a href="mailto:{EMAIL}">{EMAIL}</a><a href="{MAP}">Come raggiungerci {ARROW}</a></div>
  </div>
  <div class="wrap ft-legal"><p>© <span data-year>2026</span> Lumetra Impianti · attività di fantasia</p><a href="privacy.html">Privacy e cookie</a><p>Sito dimostrativo</p></div>
  <div class="wrap ft-demo"><p>Attività di fantasia: nomi, recapiti, prezzi e recensioni sono inventati. Sito dimostrativo realizzato da <a href="https://www.modicamichele.it">Michele Modica</a>.</p></div>
</footer>
<nav class="mobile-contact" aria-label="Contatto rapido"><a href="tel:+390000000000"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.6 3.5 9 3l1.6 4.2-2 1.4a12 12 0 0 0 6.8 6.8l1.4-2L21 15l-.5 2.4A2.5 2.5 0 0 1 18 19.5 15.5 15.5 0 0 1 4.5 6 2.5 2.5 0 0 1 6.6 3.5Z" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/></svg>Chiama</a><a href="{bar_href}">{bar_label}{ARROW}</a></nav>'''


def localize_404(html):
    """The 404 page can be served at any depth: make its local URLs root-relative."""
    html = re.sub(r'(["\s,])((?:img|assets)/)', lambda m: m.group(1) + BASE_PATH + m.group(2), html)
    return re.sub(r'href="(?!https?:|mailto:|tel:|#|/)([^"]+)"', lambda m: 'href="' + BASE_PATH + m.group(1) + '"', html)


def keep_together(text):
    """Non-breaking spaces where a line break would strand a short term: «dal 2006», «Quadri BT», «Rocca Tessera»."""
    text = re.sub(r'\b([Dd]al|[Nn]el) (\d{4})', r'\1&nbsp;\2', text)
    text = text.replace('Rocca Tessera', 'Rocca&nbsp;Tessera')
    return re.sub(r' (MT|BT)\b', r'&nbsp;\1', text)


def typographic(html):
    """Use the typographic apostrophe in text and attribute values, never inside scripts."""
    parts = re.split(r'(<script[ >].*?</script>)', html, flags=re.S)
    for i in range(0, len(parts), 2):
        parts[i] = parts[i].replace('&#x27;', '’')
        parts[i] = re.sub(r">([^<]*)<", lambda m: '>' + keep_together(m.group(1).replace("'", '’')) + '<', parts[i])
        parts[i] = re.sub(r'(content|alt|aria-label|placeholder|title|data-title|data-lead)="([^"]*)"', lambda m: f'{m.group(1)}="' + m.group(2).replace("'", '’') + '"', parts[i])
        # Desktop line breaks in headings are dropped on phones (CSS): keep a space so words never join.
        parts[i] = re.sub(r'(<h[12][^>]*>)(.*?)(</h[12]>)', lambda m: m.group(1) + re.sub(r'(?<! )<br>', ' <br>', m.group(2)) + m.group(3), parts[i], flags=re.S)
    return ''.join(parts)


def page(filename, title, description, body, active='', bodyclass='', bar=None):
    css_version = hashlib.sha256((ROOT / 'assets/site.min.css').read_bytes()).hexdigest()[:10]
    core_version = hashlib.sha256((ROOT / 'assets/core.js').read_bytes()).hexdigest()[:10]
    site_version = hashlib.sha256((ROOT / 'assets/site.js').read_bytes()).hexdigest()[:10]
    og_version = hashlib.sha256((ROOT / 'assets/og.jpg').read_bytes()).hexdigest()[:10]
    schema = {'@context': 'https://schema.org', '@type': 'Electrician', 'name': 'Lumetra Impianti (attività di fantasia)', 'telephone': TEL, 'email': EMAIL, 'address': {'@type': 'PostalAddress', 'streetAddress': 'Via delle Fornaci 8', 'addressLocality': 'Rocca Tessera', 'addressRegion': 'Piemonte', 'addressCountry': 'IT'}}
    out = f'''<!doctype html>
<html lang="it"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(description)}">
<meta name="robots" content="noindex, nofollow"><meta name="theme-color" content="#0b2034">
<meta property="og:type" content="website"><meta property="og:locale" content="it_IT">
<meta property="og:site_name" content="Lumetra Impianti"><meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(description)}"><meta property="og:image" content="{URL}/assets/og.jpg?v={og_version}">
<meta property="og:image:type" content="image/jpeg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Lumetra Impianti, impianti elettrici e tecnologici (sito dimostrativo)">
<meta property="og:url" content="{URL}/{'' if filename == 'index.html' else filename}">
<meta name="twitter:card" content="summary_large_image"><link rel="icon" href="assets/favicon.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="assets/apple-touch-icon.png">
<link rel="preload" href="assets/fonts/plex-sans-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/plex-serif-500-latin.woff2" as="font" type="font/woff2" crossorigin>
<script>document.documentElement.classList.add('js')</script><link rel="stylesheet" href="assets/site.min.css?v={css_version}">
<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>
<script src="assets/core.js?v={core_version}" defer></script><script src="assets/site.js?v={site_version}" defer></script>
</head><body class="{bodyclass}">
{header(active)}
<main id="contenuto" tabindex="-1">{body}</main>
{footer(bar)}
</body></html>'''
    if filename == '404.html':
        out = localize_404(out)
    out = typographic(out)
    (ROOT / filename).write_text(out, encoding='utf-8', newline='\n')


def crumb(section):
    return f'<p class="crumb"><a href="index.html">Home</a><span aria-hidden="true">/</span>{section}</p>'


def titleblock(title, lead, img, section, extra='', compact=False, work=None):
    """work: the project the opening photograph comes from, credited with a link."""
    if not img:
        return f'''<section class="page-hero page-hero-text" data-hero>
  <div class="wrap"><div class="page-hero-copy">{crumb(section)}<h1 class="h1">{title}</h1><p class="lead">{lead}</p>{extra}</div></div>
</section>'''
    caption = f'<figcaption><span>Lavoro realizzato · {e(work["place"])}</span><a href="lavoro-{work["slug"]}.html">{e(work["name"])}{ARROW}</a></figcaption>' if work else ''
    return f'''<section class="page-hero {'page-hero-compact' if compact else ''}" data-hero>
  <div class="wrap page-hero-grid"><div class="page-hero-copy">{crumb(section)}<h1 class="h1">{title}</h1><p class="lead">{lead}</p>{extra}</div><figure class="page-hero-photo">{image(img, '', False, sizes='(max-width: 760px) 100vw, 46vw', bleed=True)}{caption}</figure></div>
</section>'''


# One fixed label per action, wherever the action appears.
CONTACT_LABEL = 'Parliamo del progetto'
ASSIST_LABEL = 'Richiedi assistenza'
WORKS_LABEL = 'Tutti i lavori'


def cta(title='Un impianto da realizzare<br>o rinnovare?', text='Nuovo impianto, ampliamento o manutenzione: il primo passo è capire il contesto tecnico e gli obiettivi dell’intervento.', href='contatti.html', label=CONTACT_LABEL):
    return f'''<section class="cta"><div class="wrap cta-in"><div><p class="kick">Contatti</p><h2 class="h2">{title}</h2><p>{text}</p></div><div class="cta-act">{button(label, href, 'white')}<a class="cta-tel" href="tel:+390000000000"><span>Oppure al telefono:</span> <strong>{TEL}</strong></a></div></div></section>'''


# Interventions that belong to each competence, used to choose the line shown on a related project.
FOCUS_TERMS = {
    'impianti-elettrici': r'cabin|quadr|dorsal|distribuzione|linee|elettrogen|continuità|\bups\b|blindosbarra',
    'illuminazione': r'illumin',
    'fotovoltaico': r'fotovoltaic',
    'domotica': r'domotic|automazion',
    'sicurezza': r'tvcc|videosorveglianza|antintrusione|accessi',
    'antincendio': r'rivelazione fumi|antincendio',
    'diffusione-sonora': r'diffusione sonora|evacuazione|annunci',
}


def summary(items, limit=58, focus=None):
    """A short technical line: as many interventions as fit, separated by middle dots.
    With a focus, the interventions relevant to that competence come first and alone."""
    if focus:
        relevant = [x for x in items if re.search(FOCUS_TERMS[focus], x, re.I)]
        items = relevant or items
    out = items[0]
    for item in items[1:]:
        if len(out) + 3 + len(item) > limit:
            break
        out += ' · ' + item
    return out


# Card image slots: 3 columns by default, 2 in the works index and in two-card grids.
CARD_SIZES = {3: '(max-width: 760px) 100vw, (max-width: 1020px) 50vw, 33vw', 2: '(max-width: 760px) 100vw, 50vw', 'featured': '(max-width: 760px) 100vw, 55vw'}


def workcard(w, featured=False, cols=3, focus=None):
    sizes = CARD_SIZES['featured' if featured else cols]
    if w.get('plate'):
        # No photograph of the site: a small, contained product image on the brand navy.
        photo = f'<span class="work-photo work-plate">{image(w["img"], "", sizes="(max-width: 760px) 34vw, 220px")}{ARROW}</span>'
    else:
        focus_style = '--card-focus: {}; --card-focus-wide: {}'.format(*CARD_FOCUS[w['slug']]) if w['slug'] in CARD_FOCUS else ''
        photo = f'<span class="work-photo">{image(w["img"], w["name"], sizes=sizes, style=focus_style)}{ARROW}</span>'
    line = w.get('summary') or summary(w['items'], focus=focus)
    return f'''<a class="work-card {'work-featured' if featured else ''}" href="lavoro-{w['slug']}.html" data-cat="{e(w['cat'])}">{photo}<span class="work-meta">{e(w['cat'])}<span>{e(w['place'])}</span></span><h3>{e(w['name'])}</h3><span class="work-description">{e(line)}</span></a>'''


def work_grid(works, focus=None):
    return f'<div class="work-grid work-grid-{len(works)}" data-reveal>' + ''.join(workcard(x, cols=2 if len(works) == 2 else 3, focus=focus) for x in works) + '</div>'


def gallery_grid(photos):
    """photos: (name, alt) pairs. With three, the first spans the full width on phones; with two, the tiles are portrait."""
    n = len(photos)
    def slot(i):
        if n == 2:
            # Phone tiles are 4:5, so a landscape photo is drawn wider than its tile.
            w, h = MEDIA[photos[i][0]]
            return f'(max-width: 760px) {round(50 * max(1, 1.25 * w / h))}vw, 50vw'
        return '(max-width: 760px) 100vw, 33vw' if i == 0 else '(max-width: 760px) 50vw, 33vw'
    return f'<div class="wrap gallery-grid gallery-{n}" data-reveal>' + ''.join(f'<figure>{image(name, alt, sizes=slot(i))}</figure>' for i, (name, alt) in enumerate(photos)) + '</div>'


def qualifications():
    cards = ''.join(f'<div class="qualification"><h3>{e(c[0])}</h3><p>{e(c[1])}</p></div>' for c in DATA['certs'])
    return f'''<section class="qualifications section" id="qualifiche"><div class="wrap split-heading"><div><p class="kick">Qualificazioni</p><h2 class="h2">Abilitazioni e formazione del personale.</h2><p class="section-text">Le abilitazioni di legge e la formazione che servono per lavorare in sicurezza su impianti civili e industriali.</p><a class="lnk" href="{contact(servizio='Documentazione aziendale')}">Richiedi la documentazione aggiornata {ARROW}</a></div><div class="qualification-list">{cards}</div></div></section>'''


def home():
    hero = f'''<section class="home-hero" data-hero><div class="wrap hero-layout">
  <div class="hero-copy"><p class="hero-location"><span>Impianti elettrici<span class="hero-location-extra"> e tecnologici</span> · dal 1987</span></p><h1>Corrente, luce, sicurezza. <span>Un solo referente.</span></h1><p class="hero-lead">Progettiamo, installiamo e seguiamo nel tempo impianti elettrici e tecnologici per aziende, uffici, enti pubblici e case.</p><div class="hero-actions">{button(CONTACT_LABEL, style='red')}<a class="lnk lnk-light" href="lavori.html">{WORKS_LABEL} {ARROW}</a></div><p class="hero-foot">Sede a Rocca Tessera · Lavori in tutto il Piemonte</p></div>
  <figure class="hero-photo">{image('passerella', 'La passerella sul torrente illuminata di notte, un lavoro Lumetra Impianti', False, sizes='(max-width: 600px) 160vw, (max-width: 900px) 100vw, 1100px', bleed=True)}<figcaption><span>Lavoro realizzato · Rocca Tessera</span><a href="lavoro-passerella-torrente.html">Illuminazione della passerella {ARROW}</a></figcaption></figure>
</div></section>
<section class="trust-strip" aria-label="L'esperienza di Lumetra Impianti"><div class="wrap trust-grid"><p>Impiantistica civile e industriale.<br><strong>Progetto, posa, manutenzione.</strong></p><div><b>1987</b><span>Anno di fondazione</span></div><div><b>7</b><span>Competenze impiantistiche</span></div><div><b>MT e BT</b><span>Dalla cabina al punto luce</span></div></div></section>'''
    works = f'''<section class="section home-works"><div class="wrap"><div class="section-heading"><div><p class="kick">Lavori realizzati</p><h2 class="h2">Dagli stabilimenti<br>alle opere pubbliche.</h2></div><a class="lnk" href="lavori.html">{WORKS_LABEL} {ARROW}</a></div><div class="featured-works" data-reveal>{workcard(WMAP['stabilimento-assemblaggio'], True)}{workcard(WMAP['torre-uffici'])}{workcard(WMAP['campo-fotovoltaico'])}</div><div class="reference-line"><span>Altri lavori</span><a href="lavoro-residenza-anziani.html">Residenza per anziani</a><a href="lavoro-palestra-comunale.html">Palestra comunale</a><a href="lavoro-carpenteria-pesante.html">Carpenteria pesante</a><a href="lavoro-fotovoltaico-capannone.html">Fotovoltaico su capannone</a><a href="lavori.html">Tutti i {len(WORKS)} lavori {ARROW}</a></div></div></section>'''
    # Each profile leads to pertinent work, or says plainly that it opens a request.
    audience = [
        ('Aziende e attività', 'Nuovi impianti, ampliamenti e manutenzione per stabilimenti, uffici e spazi commerciali, senza perdere di vista la continuità operativa.', 'lavori.html?settore=Industria', 'Lavori per l’industria'),
        ('Enti pubblici', 'Illuminazione pubblica, strutture sanitarie ed edifici aperti al pubblico.', 'lavori.html?settore=Pubblico', 'Lavori pubblici'),
        ('Progettisti e imprese edili', 'Un referente tecnico per sviluppare e coordinare impianti elettrici e sistemi speciali in cantiere.', contact(profilo=PROFILES[2]), 'Richiesta per progettisti e imprese'),
        ('Privati e condomini', 'Impianti elettrici, fotovoltaico, domotica e sicurezza per abitazioni e parti comuni.', contact(profilo=PROFILES[3]), 'Richiesta per abitazioni e condomini'),
    ]
    rows = ''.join(f'<a href="{href}"><div><h3>{t}</h3><p>{d}</p><span class="audience-go">{go}</span></div>{ARROW}</a>' for t, d, href, go in audience)
    routes = f'''<section class="audience section"><div class="wrap audience-layout"><div><p class="kick">Per chi lavoriamo</p><h2 class="h2">Aziende, enti pubblici, progettisti e privati.</h2><p class="section-text">Stabilimenti in produzione, edifici pubblici, cantieri e abitazioni: vincoli e tempi cambiano, il rigore tecnico resta lo stesso.</p></div><div class="audience-list">{rows}</div></div></section>'''
    service_rows = ''.join(f'''<li><a href="competenza-{s['slug']}.html" data-skill="{s['slug']}"><span class="service-num">{i:02d}</span><div><h3>{e(s['name'])}</h3><p>{e(s['lead'])}</p></div>{ARROW}</a></li>''' for i, s in enumerate(SERVICES, 1))
    previews = [(s, SERVICE_PREVIEW.get(s['slug'], s['img'])) for s in SERVICES]
    service_imgs = ''.join(image(name, '', css='service-preview ' + ('is-on' if i == 0 else ''), sizes=f'(max-width: 760px) 100vw, {max(620, round(.9 * 660 * MEDIA[name][0] / MEDIA[name][1]))}px').replace('<img ', f'<img data-skill-img="{s["slug"]}" ') for i, (s, name) in enumerate(previews))
    services = f'''<section class="section services"><div class="wrap"><div class="section-heading"><div><p class="kick">Impianti e servizi</p><h2 class="h2">Sette competenze per gli impianti dell’edificio.</h2></div><p class="section-text">Elettrico, energia, controllo e protezione: sistemi diversi, progettati e coordinati per lavorare insieme nello stesso edificio.</p></div><div class="service-layout"><ol class="service-list" data-skills>{service_rows}</ol><figure class="service-photo">{service_imgs}<figcaption>Progettazione, installazione e manutenzione</figcaption></figure></div></div></section>'''
    method = f'''<section class="method section"><div class="wrap"><div class="section-heading"><div><p class="kick">Metodo</p><h2 class="h2">Prima capiamo.<br>Poi realizziamo.</h2></div><p class="section-text">Dall'esigenza iniziale all'impianto in funzione: ogni fase viene condivisa prima di procedere.</p></div><div class="method-layout"><figure>{image('schema', 'Uno schema elettrico con un relè appoggiato sopra')}</figure><ol class="method-steps"><li><span>01</span><div><h3>Sopralluogo e ascolto</h3><p>Rileviamo l'impianto esistente, l'uso degli spazi e le priorità del committente.</p></div></li><li><span>02</span><div><h3>Soluzione e proposta</h3><p>Definiamo soluzione tecnica e perimetro dell'intervento prima di iniziare.</p></div></li><li><span>03</span><div><h3>Realizzazione</h3><p>Le nostre squadre installano e coordinano le lavorazioni con il progetto e il cantiere.</p></div></li><li><span>04</span><div><h3>Assistenza nel tempo</h3><p>Controlli programmati e interventi per mantenere l'impianto efficiente.</p></div></li></ol></div></div></section>'''
    assist = f'''<section class="care-band"><div class="wrap care-layout"><figure>{image('tecnico-quadro', 'Intervento tecnico su un quadro elettrico')}</figure><div><p class="kick">Assistenza e manutenzione</p><h2 class="h2">Un buon impianto<br>va seguito nel tempo.</h2><p>Manutenzione programmata, interventi su guasti e adeguamenti: seguiamo gli impianti che abbiamo realizzato e valutiamo lo stato di quelli esistenti.</p><a class="lnk" href="assistenza.html">Scopri l'assistenza {ARROW}</a></div></div></section>'''
    about = f'''<section class="section home-about"><div class="wrap about-layout"><div><p class="kick">L'azienda</p><h2 class="h2">Da Rocca&nbsp;Tessera a tutto il&nbsp;Piemonte.</h2><p class="section-text">Dal 1987 lavoriamo nell'impiantistica civile e industriale. Agli impianti elettrici si sono aggiunti nel tempo illuminazione, fotovoltaico, domotica, sicurezza, antincendio e diffusione sonora, per industria, uffici, enti pubblici e case.</p><a class="lnk" href="azienda.html">Conosci l'azienda {ARROW}</a></div><figure>{image('sede', 'L’ingresso della sede di Lumetra Impianti')}</figure></div></section>'''
    return hero + works + routes + services + method + assist + about + cta()


# Headline for each service, and what helps to prepare the first technical conversation.
SERVICE_BENEFITS = {
 'impianti-elettrici': ('Un impianto pensato per l’attività che deve servire.', 'Potenza impegnata, schemi o planimetrie dell’impianto esistente e finestre in cui l’attività può fermarsi.'),
 'illuminazione': ('La luce giusta cambia uno spazio.', 'Planimetrie, orari di utilizzo degli ambienti e qualche fotografia dell’impianto attuale.'),
 'fotovoltaico': ('Il progetto parte dai consumi.', 'Le bollette elettriche dell’ultimo anno e alcune fotografie della copertura o dell’area disponibile.'),
 'domotica': ('Luci, clima e accessi gestiti da un unico sistema.', 'Una planimetria e l’elenco delle funzioni desiderate, come luci, clima, tapparelle e accessi.'),
 'sicurezza': ('Protezione progettata sugli spazi reali.', 'Una planimetria con ingressi e aree da proteggere, e l’indicazione dei sistemi già installati.'),
 'antincendio': ('Rilevare, segnalare, intervenire.', 'Planimetrie, destinazione d’uso dei locali e la documentazione di prevenzione incendi disponibile.'),
 'diffusione-sonora': ('Annunci, musica ed emergenza, zona per zona.', 'Una planimetria con le zone da servire e il tipo di messaggi previsti, come annunci, musica o evacuazione.')}

# Contact page heading when a request arrives already prefilled for a service.
CONTACT_TITLES = {
 'impianti-elettrici': 'Richiesta per impianti elettrici.',
 'illuminazione': 'Richiesta per un impianto di illuminazione.',
 'fotovoltaico': 'Richiesta per un impianto fotovoltaico.',
 'domotica': 'Richiesta per un impianto domotico.',
 'sicurezza': 'Richiesta per sicurezza e videosorveglianza.',
 'antincendio': 'Richiesta per rivelazione fumi e antincendio.',
 'diffusione-sonora': 'Richiesta per diffusione sonora.'}


def service(s):
    benefit, explanation = SERVICE_BENEFITS[s['slug']]
    extra = f'<div class="hero-actions">{button(CONTACT_LABEL, contact(servizio=s["short"]))}</div>'
    source = next((w for w in WORKS if w['img'] == s['img']), None)
    out = titleblock(e(s['name']), e(s['lead']), s['img'], '<a href="competenze.html">Impianti e servizi</a>', extra, work=source)
    others = ''.join(f'<li><a href="competenza-{x["slug"]}.html">{e(x["short"])}{ARROW}</a></li>' for x in SERVICES if x != s)
    items = ''.join(f'<article class="service-item"><h3>{e(a)}</h3><p>{e(b)}</p></article>' for a, b in s['items'])
    out += f'''<section class="section service-detail"><div class="wrap detail-layout"><div><h2 class="h2">{benefit}</h2><p class="detail-intro">{e(s['intro'])}</p><h2 class="h3 detail-subheading">Cosa realizziamo</h2><div class="service-items">{items}</div><div class="project-help"><h2 class="h3">Un progetto già sviluppato?</h2><p>Alla richiesta si può allegare un file, per esempio una planimetria, uno schema o il capitolato in PDF. Per più documenti è più comoda l’email.</p><a class="lnk" href="{contact(servizio=s['short'], profilo='Progettista o impresa edile')}">{CONTACT_LABEL} {ARROW}</a></div></div><aside class="detail-sidebar"><p class="kick">Cosa preparare</p><p>{explanation}</p><a class="sidebar-phone" href="tel:+390000000000">{TEL}</a><h2 class="h3">Altri impianti e servizi</h2><ul class="related-services">{others}</ul></aside></div></section>'''
    related = [WMAP[x] for x in s['works'][:3]]
    shown = {s['img']} | {w['img'] for w in related}
    gallery = [x for x in s['gallery'] if x not in shown]
    if len(gallery) >= 2:
        out += f'<section class="service-gallery">{gallery_grid([(x, "") for x in gallery])}</section>'
    if related:
        out += f'<section class="section related-works"><div class="wrap"><div class="section-heading"><div><p class="kick">Dalla competenza al cantiere</p><h2 class="h2">Lavori collegati.</h2></div><a class="lnk" href="lavori.html">{WORKS_LABEL} {ARROW}</a></div>{work_grid(related, focus=s["slug"])}</div></section>'
    return out + cta('Un intervento<br>da valutare?', 'Una breve descrizione e un recapito sono sufficienti per cominciare.', contact(servizio=s['short']))


def service_index():
    out = titleblock('Gli impianti che realizziamo.', 'Dall’energia alla sicurezza: progettiamo, realizziamo e manteniamo i sistemi che fanno funzionare l’edificio.', 'interruttori', 'Impianti e servizi')
    cards = ''.join(f'''<a class="service-card" href="competenza-{s['slug']}.html"><span class="service-card-photo">{image(s['img'], '', sizes='(max-width: 760px) 100vw, 40vw')}</span><div><span class="service-num">{i:02d}</span><h2>{e(s['name'])}</h2><p>{e(s['lead'])}</p><span class="lnk">Scopri il servizio {ARROW}</span></div></a>''' for i, s in enumerate(SERVICES, 1))
    return out + f'<section class="section"><div class="wrap service-cards" data-reveal>{cards}</div></section>' + cta()


def work_index():
    out = titleblock('Lavori realizzati.', 'Stabilimenti, uffici, strutture pubbliche e campi fotovoltaici: una selezione di interventi in Piemonte.', None, 'Lavori')
    cats = ['Tutti', 'Industria', 'Civile e terziario', 'Fotovoltaico', 'Pubblico']
    filters = ''.join(f'<button type="button" class="filter" data-filter="{c}" aria-pressed="{str(i == 0).lower()}" aria-controls="work-results">{c}</button>' for i, c in enumerate(cats))
    return out + f'''<section class="section works-section"><div class="wrap"><div class="filters-bar"><div class="filters" data-filters role="group" aria-label="Filtra i lavori per settore">{filters}</div><p class="filter-count" data-filter-count role="status" aria-live="polite">{len(WORKS)} lavori</p></div><div class="work-grid work-index" id="work-results" data-works data-reveal>{''.join(workcard(w, cols=2) for w in WORKS)}</div></div></section>''' + cta()


SECTOR_LABEL = {'Industria': 'industriale', 'Civile e terziario': 'civile e terziario', 'Pubblico': 'pubblico', 'Fotovoltaico': 'fotovoltaico'}


def work(w):
    rows = [('Committente', w['client'])] if w.get('client') else []
    rows += [('Settore', w['cat']), ('Luogo', w['place']), ('Periodo', w['year'])]
    facts = ''.join(f'<div><dt>{k}</dt><dd>{e(v)}</dd></div>' for k, v in rows)
    head = f'''<div class="project-hero-head">{crumb('<a href="lavori.html">Lavori</a>')}<h1 class="h1">{e(w['name'])}</h1><dl class="project-facts{' project-facts-4' if len(rows) > 3 else ''}">{facts}</dl></div>'''
    if w.get('plate'):
        # Without a photograph of the site, the project is presented in text alone.
        out = f'<section class="project-hero project-hero-plain" data-hero><div class="wrap">{head}</div></section>'
    else:
        focus = COVER_FOCUS.get(w['slug'], '50% 50%')
        style = f'--focus: {focus}; --focus-phone: {COVER_FOCUS_PHONE.get(w["slug"], focus)}'
        sizes = '(max-width: 760px) 100vw, 92vw'
        out = f'''<section class="project-hero" data-hero><div class="wrap">{head}<figure class="project-cover">{image(w['img'], w['name'], False, sizes=sizes, bleed=True, style=style)}</figure></div></section>'''
    items = ''.join(f'<li><span>{i:02d}</span>{e(x)}</li>' for i, x in enumerate(w['items'], 1))
    comps = ''.join(f'<a href="competenza-{x}.html">{e(SMAP[x]["short"])}{ARROW}</a>' for x in w['comp'])
    out += f'''<section class="section project-body"><div class="wrap project-layout"><div><p class="kick">Il progetto</p><p class="project-intro">{e(w['text'])}</p><h2 class="h3 project-subheading">Interventi realizzati</h2><ol class="project-items">{items}</ol><a class="lnk" href="lavori.html">{WORKS_LABEL} {ARROW}</a></div><aside class="project-sidebar"><h2 class="h3">Competenze coinvolte</h2><div class="related-services">{comps}</div><div class="project-ask"><p>Un intervento simile in programma?</p>{button(CONTACT_LABEL, contact(servizio=SMAP[w['comp'][0]]['short']))}</div></aside></div></section>'''
    related = [x for x in WORKS if x != w]
    related.sort(key=lambda x: x['cat'] != w['cat'])
    related = related[:3]
    sector = SECTOR_LABEL[w['cat']]
    heading = f'Nel settore {sector}.' if all(x['cat'] == w['cat'] for x in related) else f'Nel settore {sector} e in altri ambiti.'
    out += f'<section class="section related-works"><div class="wrap"><div class="section-heading"><div><p class="kick">Altri lavori</p><h2 class="h2">{heading}</h2></div><a class="lnk" href="lavori.html">{WORKS_LABEL} {ARROW}</a></div>{work_grid(related)}</div></section>'
    return out + cta()


def company():
    out = titleblock('Impianti a Rocca Tessera dal 1987.', 'Una ditta di impiantisti cresciuta lavorando per aziende, enti pubblici e famiglie.', 'uffici', 'Azienda')
    out += f'''<section class="section"><div class="wrap about-layout"><div><p class="kick">Identità</p><h2 class="h2">Dall’impianto elettrico ai sistemi dell’edificio.</h2><p class="section-text">Abbiamo cominciato con gli impianti elettrici. Poi gli edifici sono cambiati e abbiamo imparato il resto: illuminazione, fotovoltaico, domotica, sicurezza, antincendio e diffusione sonora.</p><p class="section-text">Lavoriamo per stabilimenti, uffici, strutture sanitarie, enti pubblici e privati in tutto il Piemonte. Lo stesso gruppo segue progetto, cantiere e assistenza.</p></div><figure>{image('schema', 'Uno schema elettrico con un relè appoggiato sopra')}</figure></div></section>
<section class="company-principles"><div class="wrap principles-grid"><article><h2>Una visione d'insieme</h2><p>Partiamo dall'edificio e dal suo utilizzo per coordinare i diversi sistemi.</p></article><article><h2>Squadre e magazzino</h2><p>Dalla sede di Rocca Tessera partono squadre, materiali e attrezzature.</p></article><article><h2>Un rapporto che continua</h2><p>Dopo la realizzazione, seguiamo l'impianto con assistenza e manutenzione.</p></article></div></section>
<section class="section"><div class="wrap"><div class="section-heading"><div><p class="kick">Storia</p><h2 class="h2">Le tappe che ci hanno portato qui.</h2></div></div><ol class="timeline"><li><span>1987</span><div><h3>Le origini</h3><p>A Rocca Tessera apre una piccola ditta di impianti elettrici civili e industriali.</p></div></li><li><span class="timeline-text">Negli anni</span><div><h3>Nuovi sistemi per l'edificio</h3><p>All'elettrico si affiancano illuminazione, sicurezza, rivelazione fumi, diffusione sonora e domotica.</p></div></li><li><span>2009</span><div><h3>L'energia solare</h3><p>Arrivano i primi impianti fotovoltaici, su capannoni e case.</p></div></li><li><span class="timeline-text">Oggi</span><div><h3>Sette competenze coordinate</h3><p>Progettazione, installazione e manutenzione per i sistemi dell'edificio.</p></div></li></ol></div></section>'''
    out += qualifications()
    clients = DATA['clients']
    entries = clients.items() if isinstance(clients, dict) else clients
    cols = ''.join(f'<div class="client-sector"><h3>{e(k)}</h3><ul>' + ''.join(f'<li>{e(n)}</li>' for n in names) + '</ul></div>' for k, names in entries)
    out += f'''<section class="section clients" id="referenze"><div class="wrap"><div class="section-heading"><div><p class="kick">Per chi lavoriamo</p><h2 class="h2">I settori dei nostri committenti.</h2></div><a class="lnk" href="lavori.html">{WORKS_LABEL} {ARROW}</a></div><div class="client-grid">{cols}</div></div></section><section class="company-gallery"><div class="wrap"><div class="section-heading"><div><p class="kick">La sede</p><h2 class="h2">Uffici, progettazione e magazzino a Rocca&nbsp;Tessera.</h2></div></div></div>{gallery_grid([('sede', 'L’ingresso della sede'), ('magazzino', 'Bobine di cavo nel piazzale del magazzino'), ('quadro-industriale', 'Un quadro cablato')])}</section>'''
    return out + cta()


def assistance():
    out = titleblock('Assistenza e manutenzione degli impianti.', 'Manutenzione programmata, guasti e adeguamenti per impianti elettrici e tecnologici, industriali e civili.', 'tecnico-quadro', 'Assistenza', f'<div class="hero-actions">{button(ASSIST_LABEL, contact(servizio="Assistenza e manutenzione"))}<a class="lnk" href="tel:+390000000000">{TEL}</a></div>')
    out += f'''<section class="section"><div class="wrap detail-layout"><div><h2 class="h2">Prendersene cura,<br>prima e dopo un guasto.</h2><p class="detail-intro">Controlli periodici, adeguamenti e interventi tecnici aiutano a mantenere l'impianto efficiente. Seguiamo gli impianti che abbiamo realizzato e valutiamo lo stato di quelli esistenti.</p><div class="service-items"><article class="service-item"><h3>Manutenzione programmata</h3><p>Verifiche e controlli su quadri, linee, illuminazione e sistemi di sicurezza, pianificati in base alle esigenze dell'impianto.</p></article><article class="service-item"><h3>Guasti e adeguamenti</h3><p>Diagnosi del problema, sostituzione dei componenti e interventi sull'impianto esistente.</p></article><article class="service-item"><h3>Impianti fotovoltaici</h3><p>Controllo dei componenti e della resa per verificare il corretto funzionamento dell'impianto.</p></article><article class="service-item"><h3>Sicurezza e antincendio</h3><p>Verifiche sui sistemi di videosorveglianza, allarme e rivelazione fumi.</p></article></div></div><aside class="assistance-contact"><p class="kick">Per organizzare un intervento</p><h2 class="h3">Cosa indicare nella richiesta.</h2><a class="sidebar-phone" href="tel:+390000000000">{TEL}</a><a class="assistance-mail" href="mailto:{EMAIL}">{EMAIL}</a><p>Comune, tipo di impianto e anomalia riscontrata. Una fotografia aiuta a inquadrare il contesto.</p><p class="assistance-note">Per le urgenze è preferibile telefonare: il modulo online non è un servizio di pronto intervento.</p>{button(ASSIST_LABEL, contact(servizio='Assistenza e manutenzione'))}</aside></div></section>'''
    return out + cta('Manutenzione<br>da programmare?', 'Valutiamo insieme lo stato dell’impianto e le attività da pianificare nel tempo.', contact(servizio='Assistenza e manutenzione'), ASSIST_LABEL)


def field(name, label, type='text', attrs='', hint='', required=False, described_extra=''):
    helptext = f'<span class="field-hint" id="{name}-hint">{hint}</span>' if hint else ''
    described = f'{name}-error' + (f' {name}-hint' if hint else '') + (f' {described_extra}' if described_extra else '')
    return f'<div class="field"><label for="{name}">{label}{" *" if required else ""}</label><input id="{name}" name="{name}" type="{type}" {attrs} {"required" if required else ""} aria-describedby="{described}">{helptext}<span class="field-error" id="{name}-error" hidden></span></div>'


def context_option(value, title, lead):
    """An option that also carries the heading shown when a link arrives with it preselected."""
    return f'<option data-title="{e(title)}" data-lead="{e(lead)}">{e(value)}</option>'


def contacts():
    out = f'''<section class="contact-intro" data-hero><div class="wrap"><div class="page-hero-copy">{crumb('Contatti')}<h1 class="h1" data-contact-title>Parliamo del progetto.</h1><p class="lead" data-contact-lead>Nuovo impianto, ampliamento o intervento sull’esistente: una breve descrizione è sufficiente per cominciare.</p></div></div></section>'''
    def service_lead(s):
        explanation = SERVICE_BENEFITS[s['slug']][1]
        return f'Descrivi brevemente l’intervento. Se disponibili, aiutano anche: {explanation[0].lower() + explanation[1:]}'
    opts = ''.join(context_option(s['short'], CONTACT_TITLES[s['slug']], service_lead(s)) for s in SERVICES)
    opts += context_option('Assistenza e manutenzione', 'Richiesta di assistenza.', 'Indica il comune, il tipo di impianto e l’anomalia riscontrata. Per le urgenze è preferibile telefonare.')
    opts += context_option('Documentazione aziendale', 'Richiesta di documentazione.', 'Abilitazioni, schede tecniche e documenti aziendali: indica cosa serve e a quale recapito inviarlo.')
    profile_context = {
        PROFILES[2]: ('Richiesta da progettisti e imprese.', 'Descrivi il progetto o il cantiere. Puoi allegare un file, come una tavola o il capitolato in PDF; per più documenti è più comoda l’email.'),
        PROFILES[3]: ('Richiesta per abitazioni e condomini.', 'Descrivi l’abitazione o le parti comuni e l’intervento da realizzare: una breve descrizione è sufficiente per cominciare.'),
    }
    profiles = ''.join(context_option(p, *profile_context[p]) if p in profile_context else f'<option>{p}</option>' for p in PROFILES)
    out += f'''<section class="contact-section"><div class="wrap contact-layout"><aside class="contact-info"><div><p class="kick">Telefono</p><a class="contact-phone" href="tel:+390000000000">{TEL}</a><p>Il modo più rapido per una prima valutazione.</p></div><div><h2>Email</h2><a class="contact-mail" href="mailto:{EMAIL}">{EMAIL}</a><p>Per documentazione tecnica e richieste articolate.</p></div><div><h2>Sede</h2><address>Via delle Fornaci 8<br>Rocca Tessera (Piemonte)</address></div><div class="contact-next"><h2>Dopo la richiesta</h2><p>Valutiamo le informazioni ricevute e, se utile, fissiamo un incontro tecnico o un sopralluogo.</p></div></aside>
<form class="form" id="richiesta" data-form-demo novalidate>
<div class="form-heading"><h2 class="h3" data-form-title>Richiesta di contatto</h2><p>I campi contrassegnati con * sono obbligatori.</p></div>
<div class="form-error-summary" data-form-errors role="alert" tabindex="-1" hidden></div>
<div data-form-fields>
<div class="field-row"><div class="field"><label for="profilo">Profilo</label><select id="profilo" name="profilo" data-prefill="profilo"><option value="">Seleziona (facoltativo)</option>{profiles}</select></div><div class="field"><label for="servizio">Servizio</label><select id="servizio" name="servizio" data-prefill="servizio"><option value="">Da valutare insieme</option>{opts}</select></div></div>
<div class="field-row">{field('nome','Nome e cognome',attrs='autocomplete="name" maxlength="120"',required=True)}{field('azienda','Azienda, ente o studio',attrs='autocomplete="organization" maxlength="160"')}</div>
{field('comune',"Comune dell'intervento",attrs='autocomplete="address-level2" maxlength="120"',required=True)}
<fieldset class="contact-channels"><legend>Recapito per la risposta * <span>Basta un'email o un numero di telefono.</span></legend><div class="field-row">{field('email','Email','email','autocomplete="email" maxlength="200"',described_extra='recapito-error')}{field('telefono','Telefono','tel','autocomplete="tel" maxlength="40" inputmode="tel"',described_extra='recapito-error')}</div><p class="field-error" id="recapito-error" hidden></p></fieldset>
<div class="field"><label for="messaggio">Descrizione dell'intervento *</label><textarea id="messaggio" name="messaggio" rows="5" required maxlength="5000" aria-describedby="messaggio-hint messaggio-error" placeholder="Tipo di edificio, impianto da realizzare o problema da risolvere…"></textarea><span class="field-hint" id="messaggio-hint">Utile indicare eventuali scadenze o riferimenti di progetto.</span><span class="field-error" id="messaggio-error" hidden></span></div>
<div class="field attachment"><label for="allegato">Foto o documento <span>(facoltativo)</span></label><div class="file-picker"><input class="file-input" id="allegato" name="allegato" type="file" accept=".pdf,.jpg,.jpeg,.png,.webp" aria-describedby="allegato-status allegato-hint allegato-error"><label class="btn btn-ghost file-button" for="allegato" aria-hidden="true">Scegli un file</label><span class="file-status" id="allegato-status" data-file-status aria-live="polite">Nessun file selezionato</span></div><span class="field-hint" id="allegato-hint">Un file PDF, JPG, PNG o WebP, fino a 10 MB. Per più documenti è più comoda l’email.</span><span class="field-error" id="allegato-error" hidden></span></div>
<p class="form-privacy">Le informazioni sono trattate secondo l’<a href="privacy.html" target="_blank" rel="noopener">informativa privacy</a>.</p>
<button class="btn btn-blue" type="submit" disabled data-submit>Rivedi la richiesta {ARROW}</button><noscript><p>Il modulo richiede JavaScript. In alternativa: telefono {TEL} o email {EMAIL}.</p></noscript>
</div><section class="form-review" data-form-ok hidden tabindex="-1" aria-labelledby="review-title"><p class="kick">Riepilogo</p><h2 class="h3" id="review-title">Controlla i dati della richiesta.</h2><dl data-review-details></dl><button class="btn btn-ghost" type="button" data-form-again>Modifica la richiesta</button></section>
<p class="demo-note">Sito dimostrativo: il modulo mostra un riepilogo e non invia dati né allegati.</p>
</form></div></section>
<section class="visit-band" id="sede"><div class="wrap visit-layout"><figure>{image('uffici', 'Gli uffici di Lumetra Impianti', bleed=True)}</figure><div><p class="kick">Sede</p><h2 class="h2">La sede di<br>Rocca Tessera.</h2><p>Via delle Fornaci 8<br>Rocca Tessera (Piemonte)</p><p>Uffici e magazzino sono nello stesso edificio. Per un incontro tecnico è meglio fissare un appuntamento.</p></div></div></section>'''
    return out


def privacy():
    # A short, ordinary notice. The owner validates it before publication: only a small draft label says so.
    sections = [
        ('Titolare del trattamento', f'Lumetra Impianti (attività di fantasia), Via delle Fornaci 8, Rocca Tessera (Piemonte). Per qualsiasi richiesta: <a href="mailto:{EMAIL}">{EMAIL}</a>.'),
        ('Dati trattati', 'Dati di navigazione, come indirizzo IP, data e ora di accesso e pagine richieste, necessari al funzionamento e alla sicurezza del sito. Dati forniti volontariamente tramite il modulo, l’email o il telefono: nome, azienda, recapiti, comune e descrizione dell’intervento, con gli eventuali allegati.'),
        ('Finalità e base giuridica', 'Rispondere alle richieste e predisporre eventuali offerte, come misure precontrattuali richieste dall’interessato (art. 6.1.b del Regolamento UE 2016/679); adempiere agli obblighi di legge (art. 6.1.c); garantire la sicurezza del sito, sulla base del legittimo interesse del titolare (art. 6.1.f).'),
        ('Conferimento e conservazione', 'Il conferimento dei dati è facoltativo, ma senza un recapito non è possibile rispondere. I dati sono conservati per il tempo necessario a gestire la richiesta e, se segue un rapporto contrattuale, per i periodi previsti dalla legge.'),
        ('Destinatari', 'Personale autorizzato del titolare e fornitori di servizi tecnici, come hosting e posta elettronica, che operano in qualità di responsabili del trattamento. I dati non sono diffusi. Eventuali trasferimenti al di fuori dell’Unione europea avvengono con le garanzie previste dal Regolamento.'),
        ('Cookie e servizi esterni', 'Il sito non utilizza cookie di profilazione né strumenti di analisi statistica. I caratteri tipografici sono ospitati sul sito stesso. Il sito non carica mappe né altri servizi esterni.'),
        ('Diritti dell’interessato', 'È possibile chiedere l’accesso ai propri dati, la rettifica, la cancellazione, la limitazione del trattamento, la portabilità o opporsi al trattamento (artt. 15–22 del Regolamento), scrivendo ai recapiti del titolare. Resta il diritto di proporre reclamo al Garante per la protezione dei dati personali.'),
    ]
    body = ''.join(f'<h2>{h}</h2><p>{p}</p>' for h, p in sections)
    return titleblock('Privacy e cookie', 'Informativa sul trattamento dei dati personali ai sensi dell’articolo 13 del Regolamento (UE) 2016/679.', None, 'Privacy') + f'''<section class="section legal-section"><div class="wrap legal-copy"><p class="legal-draft">Informativa dimostrativa: attività di fantasia</p>{body}</div></section>'''


def minify_css():
    # Safe, conservative minification; fonts are bundled to save a render-blocking request.
    css = (ROOT / 'assets/fonts.css').read_text(encoding='utf-8') + '\n' + (ROOT / 'assets/site.css').read_text(encoding='utf-8')
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.S)
    css = re.sub(r'\s+', ' ', css).strip()
    for before, after in [(' {', '{'), ('; ', ';'), (': ', ':'), (', ', ','), (' }', '}'), (';}', '}'), ('{ ', '{')]:
        css = css.replace(before, after)
    (ROOT / 'assets/site.min.css').write_text(css, encoding='utf-8')


def build():
    minify_css()
    page('index.html', 'Lumetra Impianti | Impianti elettrici e tecnologici', 'Impianti elettrici civili e industriali, illuminazione, fotovoltaico, sicurezza e antincendio a Rocca Tessera, dal progetto alla manutenzione. Sito dimostrativo.', home(), bodyclass='p-home')
    page('competenze.html', 'Impianti e servizi | Lumetra Impianti', 'Sette competenze per l’edificio: impianti elettrici, illuminazione, fotovoltaico, domotica, sicurezza, antincendio e diffusione sonora.', service_index(), 'competenze.html')
    for s in SERVICES:
        page(f'competenza-{s["slug"]}.html', f'{s["name"]} | Lumetra Impianti', s['lead'], service(s), 'competenze.html', 'p-service', bar=(CONTACT_LABEL, contact(servizio=s['short'])))
    page('lavori.html', 'Lavori realizzati | Lumetra Impianti', 'Impianti realizzati per industria, uffici, fotovoltaico ed edifici pubblici in Piemonte.', work_index(), 'lavori.html')
    for w in WORKS:
        page(f'lavoro-{w["slug"]}.html', f'{w["name"]} | Lavori Lumetra Impianti', w['text'], work(w), 'lavori.html', 'p-project')
    page('azienda.html', 'Azienda | Lumetra Impianti', 'Storia, abilitazioni e settori di Lumetra Impianti, impiantistica elettrica civile e industriale a Rocca Tessera.', company(), 'azienda.html')
    page('assistenza.html', 'Assistenza e manutenzione impianti | Lumetra Impianti', 'Manutenzione programmata, guasti e adeguamenti per impianti elettrici, fotovoltaici e sistemi di sicurezza.', assistance(), 'assistenza.html', bar=(ASSIST_LABEL, contact(servizio='Assistenza e manutenzione')))
    page('contatti.html', 'Contatti | Lumetra Impianti', 'Contatta Lumetra Impianti per nuovi impianti, ampliamenti e manutenzione. Modulo dimostrativo: nessun dato viene inviato.', contacts(), 'contatti.html', 'p-contact')
    page('privacy.html', 'Privacy e cookie | Lumetra Impianti', 'Informativa dimostrativa sul trattamento dei dati personali e sui cookie di Lumetra Impianti, attività di fantasia.', privacy())
    page('404.html', 'Pagina non trovata | Lumetra Impianti', 'La pagina cercata non è disponibile. Impianti, lavori realizzati e contatti di Lumetra Impianti.', f'<section class="not-found section" data-hero><div class="wrap"><div class="page-hero-copy"><p class="kick">Errore 404</p><h1 class="h1">Questa pagina<br>non è disponibile.</h1><p class="lead">Il collegamento potrebbe essere errato o non più attivo. Si può ripartire dalla home o dai lavori realizzati.</p><div class="hero-actions">{button("Torna alla home", "index.html")}{button(WORKS_LABEL, "lavori.html", "ghost")}</div></div></div></section>')
    files = sorted(p.name for p in ROOT.glob('*.html') if p.name != '404.html')
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + '\n'.join(f'<url><loc>{URL}/{"" if x == "index.html" else x}</loc></url>' for x in files) + '\n</urlset>\n'
    (ROOT / 'sitemap.xml').write_text(sitemap, encoding='utf-8')
    print(f'Built {len(files)+1} pages. Demo remains noindex; forms never transmit data.')


if __name__ == '__main__':
    build()
