"""Atualiza a secao 'Ultimas do portal' da home do The Watermouse (repo watermouse-home) a partir do feed.xml da Media.

Uso: python -I tools/update_home_latest.py [--push]
Reescreve o trecho entre <!--LATEST-->...<!--/LATEST--> em watermouse-home/index.html (cria a secao se nao existir)."""
import html
import pathlib
import re
import subprocess
import sys
import xml.etree.ElementTree as ET

MEDIA = pathlib.Path(__file__).resolve().parent.parent
HOME = MEDIA.parent / "watermouse-home"
N = 12

CSS = """<style>/* ultimas do portal */
.latest{border-top:1px solid var(--mist);padding-block:56px 24px;}
.latest h2{font-family:'Instrument Serif',Georgia,serif;font-weight:400;font-size:38px;line-height:1.05;margin-bottom:8px;}
.latest .sub{color:var(--graphite);max-width:62ch;margin-bottom:28px;}
.latest ul{list-style:none;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:22px 36px;}
.latest li a{display:block;border-top:1px solid var(--mist);padding-top:14px;}
.latest .cat{font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--graphite);}
.latest h3{font-family:'Instrument Serif',Georgia,serif;font-weight:400;font-size:24px;line-height:1.15;margin:6px 0;}
.latest p{color:var(--graphite);font-size:15px;line-height:1.55;}
.latest a:hover h3{text-decoration:underline;text-underline-offset:3px;}
.latest .more{margin-top:26px;}
.latest .more a{text-decoration:underline;text-underline-offset:3px;}
@media(max-width:760px){.latest ul{grid-template-columns:1fr;}}
</style>"""


def build():
    root = ET.parse(MEDIA / "feed.xml").getroot()
    items = root.findall("./channel/item")[:N]
    lis = []
    for it in items:
        g = lambda k: html.escape((it.findtext(k) or "").strip())
        lis.append(f'<li><a href="{g("link")}"><span class="cat">{g("category")}</span><h3>{g("title")}</h3><p>{g("description")}</p></a></li>')
    return ('<!--LATEST-->\n  <section class="wrap latest" aria-label="Últimas do portal">\n'
            '    <h2>Últimas do portal</h2>\n'
            '    <p class="sub">A Watermouse Media publica todos os dias notícias de ciência, tecnologia, mundo, negócios e cultura em português, com contexto para o Brasil, ressalvas sobre os limites de cada estudo e a fonte original sempre citada. Conheça a <a href="https://media.thewatermouse.com/politica-editorial.html" style="text-decoration:underline;text-underline-offset:3px">política editorial</a>.</p>\n'
            '    <ul>\n      ' + "\n      ".join(lis) + '\n    </ul>\n'
            '    <p class="more"><a href="https://media.thewatermouse.com/">Ver todas as notícias da Watermouse Media →</a></p>\n'
            '  </section>\n  <!--/LATEST-->')


def main():
    f = HOME / "index.html"
    t = f.read_text(encoding="utf-8")
    block = build()
    if "<!--LATEST-->" in t:
        t = re.sub(r"<!--LATEST-->.*?<!--/LATEST-->", lambda m: block, t, flags=re.S)
    else:
        t = t.replace('<section class="wrap how">', block + '\n\n  <section class="wrap how">', 1)
        t = t.replace("</head>", CSS + "\n</head>", 1)
    f.write_text(t, encoding="utf-8")
    print("home atualizada com", block.count("<li>"), "materias")
    if "--push" in sys.argv:
        run = lambda *a: subprocess.run(a, cwd=HOME, capture_output=True, text=True, encoding="utf-8")
        run("git", "add", "index.html")
        r = run("git", "commit", "-m", "Home: atualiza 'Ultimas do portal'\n\nCo-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>")
        if "nothing to commit" in (r.stdout + r.stderr):
            print("sem mudancas")
            return
        run("git", "pull", "-q", "--rebase")
        p = run("git", "push", "-q")
        print("push:", "ok" if p.returncode == 0 else p.stderr[-200:])


if __name__ == "__main__":
    main()
