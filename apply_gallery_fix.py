from pathlib import Path

p=Path("build.py")
s=p.read_text(encoding="utf-8")
old="render_galleries(a.get('galleries', []))"
new="render_galleries(a.get('media_blocks') or a.get('galleries', []))"
if old not in s:
    raise SystemExit("ERREUR: appel galerie attendu introuvable dans build.py")
s=s.replace(old,new)
p.write_text(s,encoding="utf-8")

css=Path("assets/css/site.css")
c=css.read_text(encoding="utf-8")
marker="/* V4.0.1 - Galeries articles */"
if marker not in c:
    c += r"""

/* V4.0.1 - Galeries articles */
.gallery-title{margin:38px 0 16px!important}
.article-gallery-mosaic{
  display:grid;
  gap:12px;
  margin:18px 0 36px;
}
.article-gallery-mosaic.cols-2{grid-template-columns:repeat(2,minmax(0,1fr))}
.article-gallery-mosaic.cols-3{grid-template-columns:repeat(3,minmax(0,1fr))}
.article-gallery-mosaic.cols-4{grid-template-columns:repeat(4,minmax(0,1fr))}
.article-gallery-mosaic figure{
  margin:0!important;
  min-width:0;
  overflow:hidden;
  border-radius:14px;
  background:#eef5f6;
}
.article-gallery-mosaic img{
  display:block;
  width:100%!important;
  height:100%!important;
  min-height:180px;
  aspect-ratio:4/3;
  object-fit:cover;
}
.article-gallery-mosaic figcaption,
.article-gallery-carousel figcaption{
  padding:8px 10px;
  font-size:12px!important;
  line-height:1.35;
}

.article-gallery-carousel{
  position:relative;
  margin:18px 0 38px;
}
.gallery-track{
  display:flex;
  overflow-x:auto;
  scroll-snap-type:x mandatory;
  scrollbar-width:none;
  border-radius:18px;
  background:#eef5f6;
}
.gallery-track::-webkit-scrollbar{display:none}
.gallery-track figure{
  flex:0 0 100%;
  width:100%;
  margin:0!important;
  scroll-snap-align:start;
}
.gallery-track img{
  display:block;
  width:100%!important;
  height:auto!important;
  max-height:680px;
  aspect-ratio:16/9;
  object-fit:contain;
  background:#eef5f6;
}
.gallery-prev,.gallery-next{
  position:absolute;
  z-index:3;
  top:50%;
  transform:translateY(-50%);
  width:46px;
  height:46px;
  border:0;
  border-radius:50%;
  background:rgba(6,31,44,.82);
  color:#fff;
  font-size:34px;
  line-height:1;
  cursor:pointer;
  box-shadow:0 5px 18px rgba(0,0,0,.22);
}
.gallery-prev{left:12px}
.gallery-next{right:12px}
.gallery-prev:hover,.gallery-next:hover{background:#061f2c}

@media(max-width:760px){
  .article-gallery-mosaic.cols-3,
  .article-gallery-mosaic.cols-4{grid-template-columns:repeat(2,minmax(0,1fr))}
  .article-gallery-mosaic img{min-height:130px}
  .gallery-prev,.gallery-next{width:40px;height:40px;font-size:29px}
}
@media(max-width:480px){
  .article-gallery-mosaic,
  .article-gallery-mosaic.cols-2,
  .article-gallery-mosaic.cols-3,
  .article-gallery-mosaic.cols-4{grid-template-columns:repeat(2,minmax(0,1fr));gap:7px}
  .article-gallery-mosaic img{min-height:105px}
}
"""
css.write_text(c,encoding="utf-8")
print("Patch appliqué : build.py + site.css")
