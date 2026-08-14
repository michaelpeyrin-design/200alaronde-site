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
    return '<header><div class="wrap"><nav><a class="brand" href="/"><img src="/assets/img/logo-200alaronde-round.png" alt="Logo 200 à la ronde"><span>200 À LA RONDE</span></a><div class="navlinks"><a href="/pages/nos-sorties.html">À venir</a><a href="/sorties.html">Archives</a><a href="/pages/documents.html">Documents</a><a href="https://roadbook.200alaronde.fr/" target="_blank" rel="noopener">Roadbook</a><a href="https://dodecaudax.200alaronde.fr/" target="_blank" rel="noopener">Dodecaudax</a><a href="https://chat.whatsapp.com/LlSf99E2niNATpJlFxNskL" target="_blank" rel="noopener">WhatsApp</a><a href="/pages/contact.html">Contact</a></div><details class="mobile-nav"><summary aria-label="Ouvrir le menu">☰</summary><div class="mobile-navlinks"><a href="https://dodecaudax.200alaronde.fr/" target="_blank" rel="noopener">Dodecaudax</a><a href="/pages/nos-sorties.html">À venir</a><a href="/sorties.html">Archives</a><a href="/pages/documents.html">Documents</a><a href="https://roadbook.200alaronde.fr/" target="_blank" rel="noopener">Roadbook</a><a href="https://chat.whatsapp.com/LlSf99E2niNATpJlFxNskL" target="_blank" rel="noopener">WhatsApp</a><a href="/pages/contact.html">Contact</a></div></details></nav></div></header>'

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
        '<link rel="stylesheet" href="/assets/css/site.css?v=3.8.2">' + jsonld_script(data)
    )
    return '<!doctype html><html lang="fr"><head>' + head + '</head><body><div class="site-version">v3.8.5</div>' + header() + '<main>' + content + '</main><footer><div class="wrap">200 à la ronde · Grenoble · Cyclisme longue distance</div></footer>' + CF_ANALYTICS + '</body></html>'

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
def sorties_months_html(p):
    if p.get("slug") != "nos-sorties" or not p.get("months"):
        return markdown_to_html(p.get("body", ""))

    parts = []
    for m in sorted(p.get("months", []), key=lambda x: int(x.get("month", 99))):
        num = int(m.get("month", 0) or 0)
        is_open = bool(m.get("registration_open")) and bool(str(m.get("registration_url", "")).strip())
        card_class = "month-open" if is_open else "month-soon"
        status = "Inscriptions ouvertes" if is_open else "À venir"
        status_class = ' open' if is_open else ''
        card = '<section class="month-card '+card_class+'" data-month="'+str(num)+'"><div class="month-name">'+esc(m.get("name", ""))+'</div><div class="month-status'+status_class+'">'+status+'</div>'
        if is_open:
            url = str(m.get("registration_url", "")).strip()
            card += '<a class="month-link" href="'+esc(url)+'" target="_blank" rel="noopener">Inscription AssoConnect</a>'
        else:
            card += '<p>Les inscriptions ne sont pas encore ouvertes.</p>'
        parts.append(card+'</section>')

    fallback_cards = ''.join(parts)
    intro = esc(p.get("intro", ""))
    note = esc(p.get("departure_note", ""))
    note_html = '<blockquote class="departure-note" id="sorties-note"><p>'+note+'</p></blockquote>' if note else '<blockquote class="departure-note" id="sorties-note" hidden><p></p></blockquote>'

    script = """<script>(function(){
const SOURCE='https://raw.githubusercontent.com/michaelpeyrin-design/200alaronde-site/main/content/pages/nos-sorties.json';
const grid=document.getElementById('sorties-grid');
const intro=document.getElementById('sorties-intro');
const note=document.getElementById('sorties-note');
function escHtml(v){return String(v??'').replace(/[&<>\\\"']/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','\\\"':'&quot;',\"'\":'&#39;'}[c]})}
function validUrl(v){try{const u=new URL(String(v||'').trim());return u.protocol==='https:'||u.protocol==='http:'}catch(e){return false}}
function render(data){
  if(!data||!Array.isArray(data.months)) return;
  if(intro&&typeof data.intro==='string') intro.textContent=data.intro;
  if(note){const txt=String(data.departure_note||'').trim();note.hidden=!txt;const p=note.querySelector('p');if(p)p.textContent=txt;}
  const currentMonth=(new Date()).getMonth()+1;
  const months=[...data.months].sort((a,b)=>Number(a.month||99)-Number(b.month||99));
  grid.innerHTML=months.map(function(m){
    const num=Number(m.month||0); if(num<currentMonth) return '';
    const url=String(m.registration_url||'').trim();
    const open=m.registration_open===true && validUrl(url);
    return '<section class=\"month-card '+(open?'month-open':'month-soon')+'\" data-month=\"'+num+'\">'+
      '<div class=\"month-name\">'+escHtml(m.name||'')+'</div>'+
      '<div class=\"month-status'+(open?' open':'')+'\">'+(open?'Inscriptions ouvertes':'À venir')+'</div>'+
      (open?'<a class=\"month-link\" href=\"'+escHtml(url)+'\" target=\"_blank\" rel=\"noopener\">Inscription AssoConnect</a>':'<p>Les inscriptions ne sont pas encore ouvertes.</p>')+
      '</section>';
  }).join('');
}
document.querySelectorAll('.month-card[data-month]').forEach(function(card){card.hidden=Number(card.dataset.month)<((new Date()).getMonth()+1)});
fetch(SOURCE+'?v='+Date.now(),{cache:'no-store'}).then(function(r){if(!r.ok)throw new Error('HTTP '+r.status);return r.json()}).then(render).catch(function(e){console.warn('Configuration sorties: fallback local utilisé',e)});
})();</script>"""

    return '<p class="sorties-intro" id="sorties-intro">'+intro+'</p><div class="sorties-grid" id="sorties-grid">'+fallback_cards+'</div>'+note_html+script

for p in load_jsons(ROOT/"content"/"pages"):
    slug=p.get("slug") or "page"; rendered_body=sorties_months_html(p)
    content='<div class="wrap page-head"><div class="eyebrow">200 à la ronde</div></div><div class="wrap content-shell"><article class="article"><h1>'+esc(p.get("title",""))+'</h1>'+rendered_body+'</article></div>'
    seo_desc=p.get("seo_description") or clean_text(p.get("intro","")) or clean_text(p.get("body",""))
    (ROOT/"pages"/f"{slug}.html").write_text(shell(p.get("title","Page"),content,seo_desc,path=f"/pages/{slug}.html",seo_title=p.get("seo_title","")),encoding="utf-8")

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

sorties = '<div class="wrap page-head"><div class="eyebrow">Archives</div><h1>Archives des sorties de l\'association</h1><p class="lead">Récits des sorties de 200 à la ronde, classées par année et par mois</p>' + year_nav + '</div><div class="wrap archives-shell">' + ''.join(year_sections) + '</div>'
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


# --- V3.7.13 : SEO technique + Cloudflare Web Analytics ---
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
    h = h.replace('site.css?v=3.8.1', 'site.css?v=3.8.2').replace('>v3.8.5<', '>v3.8.5<')
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
    h = p.read_text(encoding='utf-8').replace('site.css?v=3.8.1','site.css?v=3.8.2').replace('>v3.8.5<','>v3.8.5<')
    if 'name="robots"' not in h:
        h = h.replace('</head>','<meta name="robots" content="noindex,follow"></head>')
    if 'static.cloudflareinsights.com/beacon.min.js' not in h:
        h = h.replace('</body>', CF_ANALYTICS + '</body>')
    p.write_text(h, encoding='utf-8')

_patch_home_seo()
_patch_404()
_write_sitemap()
_write_robots()
