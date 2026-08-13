from pathlib import Path
import xml.etree.ElementTree as ET

root = Path(__file__).resolve().parent
sitemap = root / "sitemap.xml"
robots = root / "robots.txt"

if not sitemap.is_file():
    raise SystemExit("ERROR: sitemap.xml missing after build")
raw = sitemap.read_text(encoding="utf-8").lstrip()
if raw.lower().startswith("<!doctype html") or raw.lower().startswith("<html"):
    raise SystemExit("ERROR: sitemap.xml contains HTML")
if not raw.startswith('<?xml version="1.0"'):
    raise SystemExit("ERROR: sitemap.xml does not start with XML declaration")
ET.parse(sitemap)
if "<urlset" not in raw:
    raise SystemExit("ERROR: sitemap.xml has no urlset")
if not robots.is_file() or "Sitemap: https://200alaronde.fr/sitemap.xml" not in robots.read_text(encoding="utf-8"):
    raise SystemExit("ERROR: robots.txt missing or sitemap declaration invalid")
print("SEO deploy check OK: sitemap.xml is valid XML and robots.txt is present.")
