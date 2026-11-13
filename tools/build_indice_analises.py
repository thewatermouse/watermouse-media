# -*- coding: utf-8 -*-
"""Gera /analises/ (indice das analises de dados proprias) e mantem /guias/ em dia com os guias novos.
Uso (raiz do repo): python -I tools/build_indice_analises.py [--push]
- Analises = paginas publicadas cujo arquivo termina em -banco-mundial-2026.html
- Guias novos = specs em rascunhos/guias/*.json cujo .html ja existe e que ainda nao estao em guias/index.html
Seguro rodar varias vezes."""
import html, json, pathlib, re, subprocess, sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = "https://media.thewatermouse.com"
MESES = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]


def meta(h, key, attr="property"):
    m = re.search(rf'<meta {attr}="{key}" content="([^"]*)"', h)
    return html.unescape(m.group(1)) if m else ""


def row(n, href, title, desc, tag):
    return (f'<a class="grow" href="{href}"><span class="gn num">{n:02d}</span><span class="gt"><strong>{html.escape(title)}</strong>'
            f'<span class="gd">{html.escape(desc)}</span></span><span class="gm label">{html.escape(tag)}</span></a>')


def analises():
    out = []
    for f in sorted(ROOT.glob("*-banco-mundial-2026.html")):
        h = f.read_text(encoding="utf-8")
        title = meta(h, "og:title") or re.search(r"<title>(.*?)</title>", h, re.S).group(1)
        title = re.sub(r"\s*\|\s*Watermouse Media\s*$", "", title)
        desc = meta(h, "description", "name") or meta(h, "og:description")
        m = re.search(r'"datePublished":\s*"([^"]+)"', h)
        d = m.group(1) if m else "2000-01-01"
        out.append((d, f.name, title, desc))
    out.sort(reverse=True)
    return out


def build_analises():
    tpl = (ROOT / "guias" / "index.html").read_text(encoding="utf-8")
    items = analises()
    rows = "".join(row(i, "/" + fn, t, d, f"Análise · {int(dd[8:10])} {MESES[int(dd[5:7]) - 1]} {dd[:4]}") for i, (dd, fn, t, d) in enumerate(items, 1))
    desc = "Análises de dados originais da Watermouse Media: cruzamos indicadores do Banco Mundial para mostrar onde o Brasil fica em renda, saúde, desigualdade, energia, floresta e mais."
    h = tpl
    h = re.sub(r"<title>.*?</title>", "<title>Análises de dados: o Brasil comparado com o mundo | Watermouse Media</title>", h, 1, re.S)
    h = h.replace('href="https://media.thewatermouse.com/guias/"', 'href="https://media.thewatermouse.com/analises/"')
    h = h.replace('content="https://media.thewatermouse.com/guias/"', 'content="https://media.thewatermouse.com/analises/"')
    h = re.sub(r'(<meta name="description" content=")[^"]*(")', lambda m: m.group(1) + desc + m.group(2), h, 1)
    h = re.sub(r'(<meta property="og:description" content=")[^"]*(")', lambda m: m.group(1) + desc + m.group(2), h, 1)
    h = re.sub(r'(<meta property="og:title" content=")[^"]*(")', lambda m: m.group(1) + "Análises de dados" + m.group(2), h, 1)
    h = re.sub(r'<script type="application/ld\+json">.*?</script>', lambda m: m.group(0).replace('"name": "Guias"', '"name": "Análises de dados"')
               .replace("/guias/", "/analises/").replace(re.search(r'"description": "([^"]*)"', m.group(0)).group(1), desc), h, 1, re.S)
    h = h.replace('<nav class="mastnav" aria-label="Seções"><a href="/">Notícias</a><a href="/ferramentas/">Ferramentas</a></nav>',
                  '<nav class="mastnav" aria-label="Seções"><a href="/">Notícias</a><a href="/analises/">Análises</a><a href="/guias/">Guias</a><a href="/ferramentas/">Ferramentas</a></nav>')
    h = re.sub(r"<h1>Guias</h1>", "<h1>Análises de dados</h1>", h, 1)
    h = re.sub(r'<p class="lede">.*?</p>', '<p class="lede">Análises <strong>feitas por nós</strong> com dados públicos do Banco Mundial: onde o Brasil fica entre os países, com gráfico próprio, método e limites em cada texto. Quer entender como ler os gráficos? Veja os <a href="/guias/">guias</a>.</p>', h, 1, re.S)
    h = re.sub(r'<main class="wrap">.*?</main>', lambda m: f'<main class="wrap"><div class="glist">{rows}</div></main>', h, 1, re.S)
    h = h.replace("Cada guia traz o seu contexto e as ressalvas.", "Cada análise traz a fonte, o recorte de países e os limites do cálculo.")
    out = ROOT / "analises"
    out.mkdir(exist_ok=True)
    (out / "index.html").write_text(h, encoding="utf-8")
    print("analises:", len(items))
    return len(items)


def update_guias():
    p = ROOT / "guias" / "index.html"
    h = p.read_text(encoding="utf-8")
    have = set(re.findall(r'<a class="grow" href="([^"]+)"', h))
    n = len(have)
    add = []
    for sp in sorted((ROOT / "rascunhos" / "guias").glob("*.json")):
        s = json.loads(sp.read_text(encoding="utf-8"))
        href = f"/{s['slug']}.html"
        if (ROOT / f"{s['slug']}.html").exists() and href not in have:
            n += 1
            add.append(row(n, href, s["title"], s.get("dek_card") or s["dek"], f"{s['cat_label']} · {s.get('read_min', '7')} min"))
    if add:
        i = h.find("</div></main>")
        assert i > 0, "fim da lista de guias nao encontrado"
        h = h[:i] + "".join(add) + h[i:]
        p.write_text(h, encoding="utf-8")
    print("guias novos:", len(add))
    return len(add)


def sitemap():
    p = ROOT / "sitemap.xml"
    s = p.read_text(encoding="utf-8")
    loc = f"{BASE}/analises/"
    if loc not in s:
        s = s.replace("</urlset>", f"  <url><loc>{loc}</loc><changefreq>weekly</changefreq><priority>0.7</priority></url>\n</urlset>")
        p.write_text(s, encoding="utf-8")


def main():
    build_analises()
    update_guias()
    sitemap()
    if "--push" in sys.argv:
        files = ["analises/index.html", "guias/index.html", "sitemap.xml"]
        g = lambda *a: subprocess.run(["git", *a], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
        g("add", *files)
        if g("diff", "--cached", "--quiet").returncode != 0:
            g("commit", "-q", "-m", "Indice de analises e guias atualizado\n\nCo-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>")
            r = g("push")
            if r.returncode != 0:
                g("pull", "--rebase", "-q")
                r = g("push")
            print("push:", "ok" if r.returncode == 0 else "FALHOU " + r.stderr[-200:])


if __name__ == "__main__":
    main()
