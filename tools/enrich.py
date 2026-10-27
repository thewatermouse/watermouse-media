"""Insere 'Para entender o contexto' + 'Termos uteis' nas materias (idempotente).

Uso: python -I tools/enrich.py [--slug <slug>] [--dry-run]
Insere antes de <h2>As ressalvas</h2> (ou antes do bloco de atribuicao, se nao houver ressalvas)."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from enrich_data import E

ROOT = pathlib.Path(__file__).resolve().parent.parent
MARK = "<!--ctx-->"


def block(ctx, termos):
    st = 'style="font-size:17px;line-height:1.7;margin-bottom:9px"'
    li = "\n".join(f"        <li {st}><b>{t}:</b> {d}</li>" for t, d in termos)
    return (f"{MARK}\n      <h2>Para entender o contexto</h2>\n\n      {ctx.replace('</p><p>', '</p>' + chr(10) + chr(10) + '      <p>')}\n\n"
            f"      <h2>Termos úteis</h2>\n\n      <ul style=\"margin:0 0 20px;padding-left:22px\">\n{li}\n      </ul>\n\n      ")


def enrich(slug, dry=False):
    f = ROOT / f"{slug}.html"
    t = f.read_text(encoding="utf-8")
    if MARK in t:
        return "ja tem"
    ctx, termos = E[slug]
    anchor = "<h2>As ressalvas</h2>" if "<h2>As ressalvas</h2>" in t else '<div class="attrib">'
    if t.count(anchor) != 1:
        return f"ancora ambigua ({anchor}: {t.count(anchor)})"
    t = t.replace(anchor, block(ctx, termos) + anchor, 1)
    if not dry:
        f.write_text(t, encoding="utf-8")
    return "ok"


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    dry = "--dry-run" in sys.argv
    only = sys.argv[sys.argv.index("--slug") + 1] if "--slug" in sys.argv else None
    for s in E:
        if only and s != only:
            continue
        print(s, enrich(s, dry))
