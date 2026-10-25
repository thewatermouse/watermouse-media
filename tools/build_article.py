# -*- coding: utf-8 -*-
"""Cria uma materia nova a partir de um JSON de especificacao (clona uma materia real da mesma categoria).

Uso (na raiz do repo): python -I tools/build_article.py caminho/spec.json
Faz: HTML da materia + card na home (primeiro da secao) + card na pagina da categoria + sitemap.xml
     + feed.xml + links/index.html. NAO faz commit nem push (isso exige aprovacao).

Spec (JSON):
{
  "slug": "geleiras-suicas-2026",            # nome do arquivo sem .html
  "cat": "ciencia",                           # mundo | tecnologia | ciencia | negocios | cultura
  "cat_label": "Ciência",
  "title": "...", "dek": "...", "dek_card": "...", "og_desc": "...",
  "date_iso": "2026-10-24T12:00:00-03:00", "read_min": 4,
  "source_url": "https://...",                # vai em isBasedOn
  "image": "media/arquivo.jpg", "image_alt": "...", "image_caption_html": "... Foto: ..., CC0, via Wikimedia Commons.",
  "body_html": "<p>...</p><!--AD1--><h2>...</h2><p>...</p>",   # <!--AD1--> = 1o anuncio do meio; sem travessao (em-dash)
  "attrib_html": "<b>Fonte:</b> com base em <a href=... target=\"_blank\" rel=\"noopener\">...</a> ..."
}"""
import datetime as dt
import html
import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE_URL = "https://media.thewatermouse.com"
DOW = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
MON = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]
SLOT1 = ('<div class="ad-slot live" data-ad="in-article-1">\n'
         '        <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-3920760016147555" data-ad-slot="8356866030" data-ad-format="auto" data-full-width-responsive="true"></ins>\n'
         '        <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>\n'
         '      </div>')


def sub1(pat, repl, s, flags=0):
    new, n = re.subn(pat, lambda m: repl, s, count=1, flags=flags)
    assert n == 1, f"nao achei no HTML-base: {pat}"
    return new


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    spec = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))
    assert chr(0x2014) not in json.dumps(spec, ensure_ascii=False), "travessao (em-dash) proibido"
    slug, cat, label = spec["slug"], spec["cat"], spec["cat_label"]
    url = f"{BASE_URL}/{slug}.html"
    when = dt.datetime.fromisoformat(spec["date_iso"])
    date_pt = f"{when.day} de {MESES[when.month - 1]} de {when.year}"
    rfc = f"{DOW[when.weekday()]}, {when.day:02d} {MON[when.month - 1]} {when.year} {when:%H:%M:%S} -0300"
    img_abs = f"{BASE_URL}/{spec['image']}"

    # materia-base: a mais recente do feed na mesma categoria
    feed = (ROOT / "feed.xml").read_text(encoding="utf-8")
    base = None
    for it in re.findall(r"<item>(.*?)</item>", feed, re.S):
        if re.search(rf"<category>{re.escape(label)}</category>", it):
            base = re.search(r"<link>.*/([^/]+\.html)</link>", it).group(1)
            break
    assert base, f"nenhuma materia-base da categoria {label} no feed"
    t = (ROOT / base).read_text(encoding="utf-8")

    title, dek, og = html.escape(spec["title"], quote=False), spec["dek"], spec["og_desc"]
    title_a, og_a = html.escape(spec["title"]), html.escape(spec["og_desc"])  # para atributos (aspas escapadas)
    js = lambda s: json.dumps(s, ensure_ascii=False)[1:-1]  # para o JSON-LD
    JSTR = r'"(?:[^"\\]|\\.)*"'  # string JSON, aceita aspas escapadas
    t = sub1(r"<title>.*?</title>", f"<title>{title} | Watermouse Media</title>", t, re.S)
    t = sub1(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{url}">', t)
    t = sub1(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{title_a}">', t)
    t = sub1(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{og_a}">', t)
    t = sub1(r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="{url}">', t)
    t = sub1(r'<meta property="og:image" content="[^"]*">', f'<meta property="og:image" content="{img_abs}">', t)
    t = sub1(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{og_a}">', t)
    t = sub1(r'"headline": ' + JSTR, f'"headline": "{js(spec["title"])}"', t)
    t = sub1(r'"description": ' + JSTR, f'"description": "{js(spec["og_desc"])}"', t)
    t = sub1(r'"image": "[^"]*"', f'"image": "{img_abs}"', t)
    t = sub1(r'"datePublished": "[^"]*"', f'"datePublished": "{spec["date_iso"]}"', t)
    t = sub1(r'"dateModified": "[^"]*"', f'"dateModified": "{spec["date_iso"]}"', t)
    t = sub1(r'"articleSection": "[^"]*"', f'"articleSection": "{label}"', t)
    t = sub1(r'"mainEntityOfPage": "[^"]*"', f'"mainEntityOfPage": "{url}"', t)
    t = sub1(r'"isBasedOn": "[^"]*"', f'"isBasedOn": "{spec["source_url"]}"', t)
    t = sub1(r'<div class="a-cat">.*?</div>', f'<div class="a-cat">{label}</div>', t, re.S)
    t = sub1(r"<h1>.*?</h1>", f"<h1>{title}</h1>", t, re.S)
    t = sub1(r'<p class="dek">.*?</p>', f'<p class="dek">{dek}</p>', t, re.S)
    t = sub1(r'<div class="meta">.*?</div>',
             f'<div class="meta"><span>Por <b>Redação Watermouse Media</b></span><span>{date_pt}</span><span>{spec["read_min"]} min de leitura</span></div>', t, re.S)
    fig = (f'<figure class="hero-fig">\n      <img src="{spec["image"]}" alt="{html.escape(spec["image_alt"])}" loading="lazy">\n'
           f'      <figcaption>{spec["image_caption_html"]}</figcaption>\n    </figure>')
    t = sub1(r'<figure class="hero-fig">.*?</figure>', fig, t, re.S)
    body = spec["body_html"].replace("<!--AD1-->", SLOT1)
    new_body = f'<div class="body">\n      {body}\n\n      <div class="attrib">\n        {spec["attrib_html"]}\n        <span class="note">Cobertura original da Watermouse Media, com contexto para o leitor brasileiro. Os fatos são atribuídos à fonte; o texto não é uma tradução.</span>\n      </div>\n    </div>'
    t = sub1(r'<div class="body">.*?</div>(?=\s*\n\s*<div class="ad-slot(?: live)?" data-ad="in-article-2">)', new_body, t, re.S)
    (ROOT / f"{slug}.html").write_text(t, encoding="utf-8")

    # cards: copia as classes do primeiro card existente da categoria na home
    home = (ROOT / "index.html").read_text(encoding="utf-8")
    sec = home.index(f'id="{cat}"')
    first = re.search(r'<a href="[^"]+" class="card"><div class="card-img (\w+)">', home[sec:])
    cls = first.group(1)
    card = (f'<a href="{slug}.html" class="card"><div class="card-img {cls}"><img src="{spec["image"]}" alt="" loading="lazy"></div>'
            f'<span class="chip {cls}">{label}</span><h3>{title}</h3><p class="dek">{spec["dek_card"]}</p></a>')
    j = home.index('<a href="', home.index('<div class="grid">', sec))
    (ROOT / "index.html").write_text(home[:j] + card + "\n      " + home[j:], encoding="utf-8")
    cp = ROOT / f"{cat}.html"
    c = cp.read_text(encoding="utf-8")
    j = c.index('<a href="', c.index('<div class="cat-grid">'))
    cp.write_text(c[:j] + card + "\n      " + c[j:], encoding="utf-8")

    # sitemap + feed
    sm = ROOT / "sitemap.xml"; x = sm.read_text(encoding="utf-8")
    k = x.index("\n", x.index(f"<loc>{BASE_URL}/</loc>")) + 1
    x = x[:k] + f'  <url><loc>{url}</loc><lastmod>{when:%Y-%m-%d}</lastmod><changefreq>monthly</changefreq><priority>0.7</priority></url>\n' + x[k:]
    x = re.sub(rf"(<loc>{re.escape(BASE_URL)}/</loc><lastmod>)[^<]*", rf"\g<1>{when:%Y-%m-%d}", x, count=1)
    sm.write_text(x, encoding="utf-8")
    item = (f"    <item>\n      <title>{title}</title>\n      <link>{url}</link>\n      <guid isPermaLink=\"true\">{url}</guid>\n"
            f"      <pubDate>{rfc}</pubDate>\n      <category>{label}</category>\n      <description>{html.escape(spec['dek_card'], quote=False)}</description>\n    </item>\n")
    k = feed.index("    <item>")
    feed = feed[:k] + item + feed[k:]
    feed = re.sub(r"<lastBuildDate>[^<]*</lastBuildDate>", f"<lastBuildDate>{rfc}</lastBuildDate>", feed, count=1)
    (ROOT / "feed.xml").write_text(feed, encoding="utf-8")

    subprocess.run([sys.executable, "-I", str(ROOT / "tools" / "build_links.py")], check=True, cwd=ROOT)
    print(f"ok: {slug}.html (base: {base}) + cards + sitemap + feed + links")


if __name__ == "__main__":
    main()
