from pathlib import Path
import json, re, html

ROOT = Path(__file__).parent

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
    return '<header><div class="wrap"><nav><a class="brand" href="/"><img src="/assets/img/logo-200alaronde-round.png" alt="Logo 200 à la ronde"><span>200 À LA RONDE</span></a><div class="navlinks"><a href="/pages/nos-sorties.html">Nos sorties</a><a href="/sorties.html">Archives</a><a href="/pages/le-groupe.html">Documents</a><a href="https://200alaronde-roadbook.netlify.app/" target="_blank" rel="noopener">Roadbook</a><a href="https://dodecaudax200alaronde.netlify.app/" target="_blank" rel="noopener">Dodecaudax</a><a href="/pages/partenaires-amies.html">Partenaires</a><a href="/pages/contact.html">Contact</a></div></nav></div></header>'

def shell(title, content, desc=""):
    return '<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>' + esc(title) + ' - 200 à la ronde</title><meta name="description" content="' + esc(desc[:220]) + '"><link rel="stylesheet" href="/assets/css/site.css?v=3.6.2"></head><body>' + header() + '<main>' + content + '</main><footer><div class="wrap">200 à la ronde · Grenoble · Cyclisme longue distance</div></footer></body></html>'

articles = load_jsons(ROOT/"content"/"articles")
articles.sort(key=lambda x: x.get("date",""), reverse=True)

(ROOT/"articles").mkdir(exist_ok=True)
for a in articles:
    slug = a.get("slug") or re.sub(r"[^a-z0-9-]+", "-", a.get("title","").lower()).strip("-")
    body = markdown_to_html(a.get("body",""))
    featured = ""
    if a.get("featured_image"):
        featured = '<figure class="hero-image"><img src="' + esc(a["featured_image"]) + '" alt=""></figure>'
    content = '<div class="wrap page-head"><div class="eyebrow">' + esc(a.get("category","")) + ' · ' + esc(a.get("date","")) + '</div></div><div class="wrap content-shell"><article class="article"><h1>' + esc(a.get("title","")) + '</h1>' + featured + body + '</article></div>'
    (ROOT/"articles"/f"{slug}.html").write_text(shell(a.get("title","Article"), content, a.get("summary","")), encoding="utf-8")

(ROOT/"pages").mkdir(exist_ok=True)
for p in load_jsons(ROOT/"content"/"pages"):
    slug = p.get("slug") or "page"
    content = '<div class="wrap page-head"><div class="eyebrow">200 à la ronde</div></div><div class="wrap content-shell"><article class="article"><h1>' + esc(p.get("title","")) + '</h1>' + markdown_to_html(p.get("body","")) + '</article></div>'
    (ROOT/"pages"/f"{slug}.html").write_text(shell(p.get("title","Page"), content), encoding="utf-8")

cards = []
for a in articles:
    slug = a.get("slug","")
    cards.append('<article class="post-card"><div class="eyebrow">' + esc(a.get("category","")) + ' · ' + esc(a.get("date","")) + '</div><h2><a href="/articles/' + esc(slug) + '.html">' + esc(a.get("title","")) + '</a></h2><p>' + esc(a.get("summary","")) + '</p><a class="read" href="/articles/' + esc(slug) + '.html">Lire l’article →</a></article>')

sorties = '<div class="wrap page-head"><div class="eyebrow">Archives</div><h1>Les sorties</h1><p class="lead">Récits, brevets et aventures longue distance de 200 à la ronde.</p></div><div class="wrap posts-grid">' + "".join(cards) + '</div>'
(ROOT/"sorties.html").write_text(shell("Les sorties", sorties), encoding="utf-8")
print("Site généré :", len(articles), "articles")


# --- V3.6.3 : accueil dynamique, jusqu'à 25 articles classés par date ---
def _home_first_image(body):
    m = re.search(r'<img[^>]+src=["\']([^"\']+)["\']', body or "", re.I)
    return m.group(1) if m else ""

def _home_card(a):
    img = a.get("featured_image") or _home_first_image(a.get("body",""))
    img_tag = '<img src="' + esc(img) + '" alt="" loading="lazy">' if img else ""
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
