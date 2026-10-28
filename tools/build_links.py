# -*- coding: utf-8 -*-
"""Gera links/index.html (a pagina de "link na bio" do Instagram) a partir do feed.xml.

Uso (na raiz do repo): python -I tools/build_links.py
Rode de novo sempre que publicar uma materia (a rotina noticias-diario faz isso).
Pega os N itens mais recentes do feed, monta a lista e marca os links com UTM do Instagram."""
import html
import pathlib
import re
import sys

N = 6
ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = "https://media.thewatermouse.com"
UTM = "utm_source=instagram&utm_medium=bio&utm_campaign=link_na_bio"

feed = (ROOT / "feed.xml").read_text(encoding="utf-8")
items = re.findall(r"<item>(.*?)</item>", feed, re.S)[:N]
rows = []
for it in items:
    title = re.search(r"<title>(.*?)</title>", it, re.S).group(1).strip()
    link = re.search(r"<link>(.*?)</link>", it, re.S).group(1).strip()
    cat = re.search(r"<category>(.*?)</category>", it, re.S).group(1).strip()
    rows.append(f'      <a class="item" href="{link}?{UTM}"><span class="cat">{cat}</span>'
                f'<span class="ttl">{title}</span></a>')

# mascote e bloco de cookies/GA copiados de uma materia real (mesma marca, mesmo consentimento)
art = (ROOT / "encelado-oceano-vida-2026.html").read_text(encoding="utf-8")
mascot = re.search(r'<svg viewBox="0 0 220 200".*?</svg>', art, re.S).group(0)
mascot = mascot.replace('width="38" height="35" class="wm-mascot"', 'width="84" height="76" class="wm-mascot"')
ga = re.search(r"<!-- Google (?:Analytics 4|Tag Manager) .*?</script>", art, re.S).group(0)
cookie = re.search(r'<div id="wm-cookie".*?</script>', art, re.S).group(0)

PAGE = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="robots" content="noindex,follow">
{ga}
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Watermouse Media: links</title>
<link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=Instrument+Serif:ital@0;1&family=Newsreader:ital,opsz,wght@0,6..72,300..700&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="canonical" href="{BASE}/">
<style>
  :root{{--bg:#F8F8F9;--surface:#fff;--ink:#0D0D0F;--muted:#55585F;--faint:#8A8D94;--cobalt:#2337FF;--line:rgba(13,13,15,.12);}}
  *,*::before,*::after{{margin:0;padding:0;box-sizing:border-box;}}
  body{{font-family:'Newsreader',Georgia,serif;background:var(--bg);color:var(--ink);-webkit-font-smoothing:antialiased;line-height:1.5;}}
  a{{color:inherit;text-decoration:none;}}
  .wrap{{max-width:480px;margin:0 auto;padding:36px 20px 56px;}}
  header{{text-align:center;margin-bottom:26px;}}
  .wm-mascot{{display:block;margin:0 auto 14px;}}
  h1{{font-family:'DM Serif Display',serif;font-weight:400;font-size:32px;letter-spacing:-.02em;line-height:1.05;}}
  h1 em{{font-style:italic;}} h1 i{{font-style:normal;color:var(--cobalt);}}
  .tag{{font-family:'Instrument Serif',serif;font-style:italic;font-size:21px;color:var(--muted);margin-top:8px;}}
  .btn{{display:block;text-align:center;border-radius:2px;padding:15px 18px;margin-bottom:10px;font-family:'IBM Plex Mono',monospace;font-size:13.5px;font-weight:500;letter-spacing:.04em;text-transform:uppercase;border:1px solid var(--ink);}}
  .btn.solid{{background:var(--ink);color:#F8F8F9;}} .btn.solid:active,.btn.solid:hover{{background:var(--cobalt);border-color:var(--cobalt);}}
  .btn.ghost{{background:transparent;color:var(--ink);}} .btn.ghost:hover{{border-color:var(--cobalt);color:var(--cobalt);}}
  .hero{{display:block;background:var(--cobalt);color:#fff;border-radius:2px;padding:18px 18px 16px;margin-bottom:12px;}}
  .hero .k{{display:block;font-family:'IBM Plex Mono',monospace;font-size:11px;letter-spacing:.1em;text-transform:uppercase;opacity:.8;margin-bottom:6px;}}
  .hero .t{{display:block;font-family:'DM Serif Display',serif;font-size:24px;line-height:1.1;}}
  .hero .d{{display:block;font-size:14px;opacity:.88;margin-top:6px;}}
  .hero:hover{{background:var(--ink);}}
  .lbl{{font-family:'IBM Plex Mono',monospace;font-size:11.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--faint);margin:30px 0 10px;}}
  .item{{display:block;background:var(--surface);border:1px solid var(--line);border-radius:2px;padding:14px 16px;margin-bottom:9px;}}
  .item:hover{{border-color:var(--cobalt);}}
  .item .cat{{display:block;font-family:'IBM Plex Mono',monospace;font-size:10.5px;font-weight:500;letter-spacing:.1em;text-transform:uppercase;color:var(--cobalt);margin-bottom:5px;}}
  .item .ttl{{font-family:'DM Serif Display',serif;font-size:19px;line-height:1.18;letter-spacing:-.01em;}}
  footer{{margin-top:34px;text-align:center;font-family:'IBM Plex Mono',monospace;font-size:11px;color:var(--faint);}}
  footer a{{color:var(--ink);text-decoration:underline;text-underline-offset:3px;}}
  .wm-cookie{{position:fixed;left:12px;right:12px;bottom:12px;z-index:9999;max-width:480px;margin:0 auto;background:#08080A;color:#F8F8F9;border:1px solid rgba(248,248,249,.16);border-radius:2px;padding:14px 16px;display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap;}}
  .wm-cookie[hidden]{{display:none!important;}}
  .wm-cookie-text{{font-size:12.5px;line-height:1.5;color:rgba(248,248,249,.82);flex:1;min-width:200px;}}
  .wm-cookie-text a{{color:#8D98FF;}}
  .wm-cookie-actions{{display:flex;gap:8px;}}
  .wm-cookie-btn{{font-family:inherit;font-size:13px;font-weight:500;border-radius:2px;padding:9px 16px;cursor:pointer;border:none;}}
  .wm-cookie-btn.ghost{{background:transparent;color:rgba(248,248,249,.72);border:1px solid rgba(248,248,249,.24);}}
  .wm-cookie-btn.solid{{background:#2337FF;color:#fff;}}
</style>
</head>
<body>
<div class="wrap">
  <header>
    {mascot}
    <h1>Watermouse <em>Media</em><i>.</i></h1>
    <p class="tag">As notícias do mundo que não chegam aqui.</p>
  </header>

  <a class="hero" href="{BASE}/orcamento/?{UTM}"><span class="k">Simulador</span><span class="t">Se eu fosse presidente: monte o orçamento</span><span class="d">R$ 2,61 trilhões. Onde você poria o dinheiro?</span></a>
  <a class="btn solid" href="{BASE}/?{UTM}">Todas as notícias</a>
  <a class="btn ghost" href="{BASE}/?{UTM}#newsletter">Receber no e-mail</a>

  <div class="lbl">Ferramentas</div>
  <nav>
      <a class="item" href="{BASE}/mais-ou-menos/?{UTM}"><span class="cat">Jogo diário</span><span class="ttl">Mais ou menos? Dez rodadas de números do mundo</span></a>
      <a class="item" href="{BASE}/brasil-em-100/?{UTM}"><span class="cat">Explicador</span><span class="ttl">O Brasil em 100 pessoas (e onde você aparece)</span></a>
      <a class="item" href="{BASE}/comparar/?{UTM}"><span class="cat">Comparador</span><span class="ttl">Compare dois países em 21 indicadores</span></a>
      <a class="item" href="{BASE}/orcamento/?{UTM}"><span class="cat">Simulador</span><span class="ttl">Se eu fosse presidente: monte o orçamento federal</span></a>
  </nav>

  <div class="lbl">Últimas matérias</div>
  <nav>
{chr(10).join(rows)}
  </nav>

  <footer>© 2026 Watermouse Media · parte do <a href="https://thewatermouse.com">The Watermouse</a></footer>
</div>
{cookie}
</body>
</html>
"""
out = ROOT / "links" / "index.html"
out.parent.mkdir(exist_ok=True)
out.write_text(PAGE, encoding="utf-8")
sys.stdout.reconfigure(encoding="utf-8")
print(f"links/index.html gerado com {len(rows)} materias")
