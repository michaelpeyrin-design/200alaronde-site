from pathlib import Path
import json, re, html

ROOT = Path(__file__).parent
SITE_URL = "https://200alaronde.fr"
SITE_NAME = "200 à la ronde"
DEFAULT_DESC = "200 à la ronde, association cycliste grenobloise dédiée aux sorties longue distance de 200 km et plus, Dodecaudax et BRM."
DEFAULT_IMAGE = "/assets/img/logo-200alaronde-round.png"
CF_ANALYTICS = "<script type='module' src='https://static.cloudflareinsights.com/beacon.min.js' data-cf-beacon='{\"token\": \"85a4af337e704192a2b01df76a118d29\"}'></script>"

def load_jsons(folder):
    out = []
    for p in folder.glob("*.json"):
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
            if d.get("published", True):
                out.append(d)
        except Exception as e:
            print("Erreur", p, e)
    return out

def esc(s):
    return html.escape(str(s or ""))

def inline_md(s):
    s = esc(s)
    s = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', r'<img src="\2" alt="\1">', s)
    s = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', s)
    s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'\*(.+?)\*', r'<em>\1</em>', s)
    return s

def markdown_to_html(text):
    if not text:
        return ""
    if re.search(r"<(p|h[1-6]|figure|div|ul|ol|blockquote|img|table)\b", text, re.I):
        return text
    lines = text.replace("\r\n", "\n").split("\n")
    out, in_ul, in_ol = [], False, False
    for line in lines:
        if not line.strip():
            if in_ul:
                out.append("</ul>"); in_ul = False
            if in_ol:
                out.append("</ol>"); in_ol = False
            continue
        m = re.match(r"^(#{1,4})\s+(.+)$", line)
        if m:
            n = len(m.group(1))
            out.append(f"<h{n}>{inline_md(m.group(2))}</h{n}>")
            continue
        m = re.match(r"^\s*[-*]\s+(.+)$", line)
        if m:
            if in_ol:
                out.append("</ol>"); in_ol = False
            if not in_ul:
                out.append("<ul>"); in_ul = True
            out.append("<li>" + inline_md(m.group(1)) + "</li>")
            continue
        m = re.match(r"^\s*\d+\.\s+(.+)$", line)
        if m:
            if in_ul:
                out.append("</ul>"); in_ul = False
            if not in_ol:
                out.append("<ol>"); in_ol = True
            out.append("<li>" + inline_md(m.group(1)) + "</li>")
            continue
        if in_ul:
            out.append("</ul>"); in_ul = False
        if in_ol:
            out.append("</ol>"); in_ol = False
        out.append("<p>" + inline_md(line) + "</p>")
    if in_ul:
        out.append("</ul>")
    if in_ol:
        out.append("</ol>")
    return "\n".join(out)

def header():
    return '<header><div class="wrap"><nav><a class="brand" href="/"><img src="/assets/img/logo-200alaronde-round.png" alt="Logo 200 à la ronde"><span>200 À LA RONDE</span></a><div class="navlinks"><a href="/pages/nos-sorties.html">Nos sorties</a><a href="/sorties.html">Archives</a><a href="/pages/le-groupe.html">Documents</a><a href="https://200alaronde-roadbook.netlify.app/" target="_blank" rel="noopener">Roadbook</a><a href="https://dodecaudax200alaronde.netlify.app/" target="_blank" rel="noopener">Dodecaudax</a><a href="https://chat.whatsapp.com/LlSf99E2niNATpJlFxNskL" target="_blank" rel="noopener">WhatsApp</a><a href="/pages/contact.html">Contact</a></div><details class="mobile-nav"><summary aria-label="Ouvrir le menu">☰</summary><div class="mobile-navlinks"><a href="https://dodecaudax200alaronde.netlify.app/" target="_blank" rel="noopener">Dodecaudax</a><a href="/pages/nos-sorties.html">Nos sorties</a><a href="/sorties.html">Archives</a><a href="/pages/le-groupe.html">Documents</a><a href="https://200alaronde-roadbook.netlify.app/" target="_blank" rel="noopener">Roadbook</a><a href="https://chat.whatsapp.com/LlSf99E2niNATpJlFxNskL" target="_blank" rel="noopener">WhatsApp</a><a href="/pages/contact.html">Contact</a></div></details></nav></div></header>'

def clean_text(s):
    s = re.sub(r'<[^>]+>', ' ', str(s or ''))
    return re.sub(r'\s+', ' ', s).strip()

def absolute_url(path):
    if not path:
        return SITE_URL + DEFAULT_IMAGE
    if str(path).startswith(('http://','https://')):
        return str(path)
    return SITE_URL + ('/' if not str(path).startswith('/') else '') + str(path)

def meta_description(desc, fallback=''):
    text = clean_text(desc) or clean_text(fallback) or DEFAULT_DESC
    return text[:160].rstrip()

def jsonld_script(data):
    return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False) + '</script>'

def shell(title, content, desc="", path="/", image="", kind="WebPage", date="", seo_title=""):
    page_title = (seo_title or title or SITE_NAME).strip()
    full_title = page_title if SITE_NAME.lower() in page_title.lower() else page_title + ' - ' + SITE_NAME
    canonical = SITE_URL + (path if path.startswith('/') else '/' + path)
    description = meta_description(desc, title)
    og_image = absolute_url(image or DEFAULT_IMAGE)
    data = {
        '@context':'https://schema.org', '@type': kind, 'name': page_title, 'headline': page_title,
        'description': description, 'url': canonical, 'inLanguage':'fr-FR', 'image': og_image,
        'publisher': {'@type':'Organization','name':SITE_NAME,'url':SITE_URL,'logo':{'@type':'ImageObject','url':absolute_url(DEFAULT_IMAGE)}}
    }
    if kind == 'Article' and date:
        data['datePublished'] = date
        data['dateModified'] = date
        data['author'] = {'@type':'Organization','name':SITE_NAME}
    head = (
        '<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
        '<title>' + esc(full_title) + '</title><meta name="description" content="' + esc(description) + '">'
        '<link rel="canonical" href="' + esc(canonical) + '">'
        '<meta property="og:locale" content="fr_FR"><meta property="og:site_name" content="' + SITE_NAME + '">'
        '<meta property="og:type" content="' + ('article' if kind == 'Article' else 'website') + '">'
        '<meta property="og:title" content="' + esc(full_title) + '"><meta property="og:description" content="' + esc(description) + '">'
        '<meta property="og:url" content="' + esc(canonical) + '"><meta property="og:image" content="' + esc(og_image) + '">'
        '<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="' + esc(full_title) + '">'
        '<meta name="twitter:description" content="' + esc(description) + '"><meta name="twitter:image" content="' + esc(og_image) + '">'
        '<link rel="stylesheet" href="/assets/css/site.css?v=3.7.11">' + jsonld_script(data)
    )
    return '<!doctype html><html lang="fr"><head>' + head + '</head><body><div class="site-version">v3.7.11</div>' + header() + '<main>' + content + '</main><footer><div class="wrap">200 à la ronde · Grenoble · Cyclisme longue distance</div></footer>' + CF_ANALYTICS + '</body></html>'

articles = load_jsons(ROOT/"content"/"articles")
articles.sort(key=lambda x: x.get("date",""), reverse=True)

(ROOT/"articles").mkdir(exist_ok=True)
for a in articles:
    slug = a.get("slug") or re.sub(r"[^a-z0-9-]+", "-", a.get("title","").lower()).strip("-")
    body = markdown_to_html(a.get("body",""))
    featured = ""
    if a.get("featured_image"):
        featured = '<figure class="hero-image"><img src="' + esc(a["featured_image"]) + '" alt="' + esc(a.get("title","")) + '" fetchpriority="high"></figure>'
    content = '<div class="wrap page-head"><div class="eyebrow">' + esc(a.get("category","")) + ' · ' + esc(a.get("date","")) + '</div></div><div class="wrap content-shell"><article class="article"><h1>' + esc(a.get("title","")) + '</h1>' + featured + body + '</article></div>'
    seo_desc = a.get("seo_description") or a.get("summary","") or clean_text(a.get("body",""))
    (ROOT/"articles"/f"{slug}.html").write_text(shell(a.get("title","Article"), content, seo_desc, path=f"/articles/{slug}.html", image=a.get("featured_image", ""), kind="Article", date=a.get("date", ""), seo_title=a.get("seo_title", "")), encoding="utf-8")

(ROOT/"pages").mkdir(exist_ok=True)
for p in load_jsons(ROOT/"content"/"pages"):
    slug = p.get("slug") or "page"
    content = '<div class="wrap page-head"><div class="eyebrow">200 à la ronde</div></div><div class="wrap content-shell"><article class="article"><h1>' + esc(p.get("title","")) + '</h1>' + markdown_to_html(p.get("body","")) + '</article></div>'
    seo_desc = p.get("seo_description") or clean_text(p.get("body",""))
    (ROOT/"pages"/f"{slug}.html").write_text(shell(p.get("title","Page"), content, seo_desc, path=f"/pages/{slug}.html", seo_title=p.get("seo_title", "")), encoding="utf-8")

MONTHS_FR = {1:"Janvier",2:"Février",3:"Mars",4:"Avril",5:"Mai",6:"Juin",7:"Juillet",8:"Août",9:"Septembre",10:"Octobre",11:"Novembre",12:"Décembre"}

def _archive_summary(a):
    summary = a.get("summary","") or re.sub(r'<[^>]+>', ' ', a.get("body",""))
    summary = re.sub(r'\s+', ' ', summary).strip()
    return summary[:177].rstrip() + "…" if len(summary) > 180 else summary

def _archive_first_image(body):
    m = re.search(r'<img[^>]+src=["\']([^"\']+)["\']', body or "", re.I)
    return m.group(1) if m else ""

def _archive_card(a):
    slug = esc(a.get("slug",""))
    d = a.get("date","")
    try:
        y,m,day = [int(x) for x in d.split("-")[:3]]
        date_fr = f"{day:02d}/{m:02d}/{y}"
    except Exception:
        date_fr = d
    img = a.get("featured_image") or _archive_first_image(a.get("body",""))
    media = ('<a class="archive-media" href="/articles/' + slug + '.html"><img src="' + esc(img) + '" alt="' + esc(a.get("title","")) + '" loading="lazy" decoding="async"></a>') if img else ''
    return ('<article class="archive-card">' + media + '<div class="archive-card-body"><div class="archive-card-top"><span class="archive-date">' + esc(date_fr) + '</span></div>'
            '<div class="archive-cat">' + esc(a.get("category","")) + '</div><h3>' + esc(a.get("title","")) + '</h3>'
            '<p>' + esc(_archive_summary(a)) + '</p><a class="archive-link" href="/articles/' + slug + '.html">Lire le récit</a></div></article>')

groups = {}
for a in articles:
    # Archives : uniquement les articles explicitement sélectionnés dans l’administration.
    if not a.get("show_in_archives", False):
        continue
    try:
        y,m,_ = [int(x) for x in a.get("date","").split("-")[:3]]
    except Exception:
        continue
    groups.setdefault(y, {}).setdefault(m, []).append(a)

years = sorted(groups, reverse=True)
year_nav = '<div class="archive-year-nav">' + ''.join('<a href="#annee-' + str(y) + '">' + str(y) + '</a>' for y in years) + '</div>'
year_sections = []
for y in years:
    months = []
    year_count = sum(len(v) for v in groups[y].values())
    for m in sorted(groups[y], reverse=True):
        items = groups[y][m]
        label = 'publication' if len(items)==1 else 'publications'
        months.append('<section class="archive-month-section"><div class="archive-month-head"><h3>' + MONTHS_FR[m] + '</h3><span>' + str(len(items)) + ' ' + label + '</span></div><div class="archive-cards">' + ''.join(_archive_card(a) for a in items) + '</div></section>')
    label = 'publication' if year_count==1 else 'publications'
    year_sections.append('<section class="archive-year" id="annee-' + str(y) + '"><div class="archive-year-head"><h2>' + str(y) + '</h2><span>' + str(year_count) + ' ' + label + '</span></div>' + ''.join(months) + '</section>')

sorties = '<div class="wrap page-head"><div class="eyebrow">Archives</div><h1>Les sorties</h1><p class="lead">Récits, brevets et aventures longue distance de 200 à la ronde, classés par année et par mois.</p>' + year_nav + '</div><div class="wrap archives-shell">' + ''.join(year_sections) + '</div>'
(ROOT/"sorties.html").write_text(shell("Les sorties", sorties, "Archives des sorties longue distance, Dodecaudax et BRM de 200 à la ronde, classées par année et par mois.", path="/sorties.html"), encoding="utf-8")
print("Site généré :", len(articles), "articles")


# --- V3.6.3 : accueil dynamique, jusqu'à 25 articles classés par date ---
def _home_first_image(body):
    m = re.search(r'<img[^>]+src=["\']([^"\']+)["\']', body or "", re.I)
    return m.group(1) if m else ""

def _home_card(a):
    img = a.get("featured_image") or _home_first_image(a.get("body",""))
    img_tag = '<img src="' + esc(img) + '" alt="' + esc(a.get("title","")) + '" loading="lazy" decoding="async">' if img else ""
    summary = a.get("summary","") or re.sub(r'<[^>]+>', ' ', a.get("body",""))
    summary = re.sub(r'\s+', ' ', summary).strip()
    if len(summary) > 220:
        summary = summary[:219].rstrip() + "…"
    slug = a.get("slug","")
    return (
        '<article class="card">' + img_tag +
        '<div class="card-body">'
        '<div class="meta">' + esc(a.get("date","")) + ' · ' + esc(a.get("category","")) + '</div>'
        '<h3>' + esc(a.get("title","")) + '</h3>'
        '<p>' + esc(summary) + '</p>'
        '<a class="more" href="/articles/' + esc(slug) + '.html">Lire le récit →</a>'
        '</div></article>'
    )

home_path = ROOT/"index.html"
if home_path.exists():
    home = home_path.read_text(encoding="utf-8")
    block = (
        '<!-- HOME_ARTICLES_START -->'
        '<div class="grid">' + "".join(_home_card(a) for a in articles[:25]) + '</div>'
        '<div class="actions"><a class="btn" href="/sorties.html">Voir tous les articles</a></div>'
        '<!-- HOME_ARTICLES_END -->'
    )
    if '<!-- HOME_ARTICLES_START -->' in home:
        home = re.sub(r'<!-- HOME_ARTICLES_START -->.*?<!-- HOME_ARTICLES_END -->', block, home, count=1, flags=re.S)
    home_path.write_text(home, encoding="utf-8")


# --- V3.6.4 : suppression des boutons d’action du hero de la page d’accueil ---


# --- V3.7.11 : SEO technique + Cloudflare Web Analytics ---
def _published_routes():
    routes = [("/", "1.0"), ("/sorties.html", "0.8")]
    for p in load_jsons(ROOT/"content"/"pages"):
        slug = p.get("slug") or "page"
        routes.append((f"/pages/{slug}.html", "0.8"))
    for a in articles:
        slug = a.get("slug") or re.sub(r"[^a-z0-9-]+", "-", a.get("title","").lower()).strip("-")
        routes.append((f"/articles/{slug}.html", "0.7"))
    return routes

def _write_sitemap():
    urls = []
    for path, priority in _published_routes():
        urls.append('  <url><loc>' + esc(SITE_URL + path) + '</loc><priority>' + priority + '</priority></url>')
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + '\n'.join(urls) + '\n</urlset>\n'
    sitemap_path = ROOT / "sitemap.xml"
    tmp_path = ROOT / "sitemap.xml.tmp"
    tmp_path.write_text(xml, encoding="utf-8")
    tmp_path.replace(sitemap_path)
    # Fail the Netlify build rather than deploy an HTML/fallback response as sitemap.
    check = sitemap_path.read_text(encoding="utf-8").lstrip()
    if not check.startswith('<?xml version="1.0"') or '<urlset' not in check:
        raise RuntimeError("sitemap.xml generation failed: valid XML sitemap was not produced")

def _write_robots():
    robots = "User-agent: *\nAllow: /\nDisallow: /admin/\n\nSitemap: " + SITE_URL + "/sitemap.xml\n"
    robots_path = ROOT / "robots.txt"
    robots_path.write_text(robots, encoding="utf-8")

def _patch_home_seo():
    p = ROOT/"index.html"
    if not p.exists(): return
    h = p.read_text(encoding="utf-8")
    h = h.replace('site.css?v=3.7.5', 'site.css?v=3.7.11').replace('>v3.7.5<', '>v3.7.11<')
    h = re.sub(r'<link rel="canonical"[^>]*>', '', h)
    h = re.sub(r'<meta property="og:[^"]+"[^>]*>', '', h)
    h = re.sub(r'<meta name="twitter:[^"]+"[^>]*>', '', h)
    h = re.sub(r'<script type="application/ld\+json">.*?</script>', '', h, flags=re.S)
    h = h.replace(CF_ANALYTICS, '')
    canonical = SITE_URL + '/'
    desc = DEFAULT_DESC
    data = {'@context':'https://schema.org','@type':'WebSite','name':SITE_NAME,'url':SITE_URL,'description':desc,'inLanguage':'fr-FR','publisher':{'@type':'Organization','name':SITE_NAME,'url':SITE_URL,'logo':{'@type':'ImageObject','url':absolute_url(DEFAULT_IMAGE)}}}
    seo = ('<link rel="canonical" href="' + canonical + '">'
           '<meta property="og:locale" content="fr_FR"><meta property="og:site_name" content="' + SITE_NAME + '"><meta property="og:type" content="website">'
           '<meta property="og:title" content="200 à la ronde — Cyclisme longue distance"><meta property="og:description" content="' + esc(desc) + '">'
           '<meta property="og:url" content="' + canonical + '"><meta property="og:image" content="' + absolute_url(DEFAULT_IMAGE) + '">'
           '<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="200 à la ronde — Cyclisme longue distance">'
           '<meta name="twitter:description" content="' + esc(desc) + '"><meta name="twitter:image" content="' + absolute_url(DEFAULT_IMAGE) + '">' + jsonld_script(data))
    h = h.replace('</head>', seo + '</head>')
    h = h.replace('</body>', CF_ANALYTICS + '</body>')
    p.write_text(h, encoding="utf-8")

def _patch_404():
    p = ROOT/"404.html"
    if not p.exists(): return
    h = p.read_text(encoding='utf-8').replace('site.css?v=3.7.5','site.css?v=3.7.11').replace('>v3.7.5<','>v3.7.11<')
    if 'name="robots"' not in h:
        h = h.replace('</head>','<meta name="robots" content="noindex,follow"></head>')
    if 'static.cloudflareinsights.com/beacon.min.js' not in h:
        h = h.replace('</body>', CF_ANALYTICS + '</body>')
    p.write_text(h, encoding='utf-8')

_patch_home_seo()
_patch_404()
_write_sitemap()
_write_robots()
