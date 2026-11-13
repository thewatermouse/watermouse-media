"""Insere bloco de analise propria (Por que importa, Em numeros, FAQ, Leitura) antes de <!--ctx--> (idempotente).
Dados em tools/aprof/*.py (dict D[slug] = dict(why, numeros, faq, leia)).
Uso: python -I tools/aprofundar.py [--dry-run]"""
import pathlib, sys, glob, importlib.util
ROOT = pathlib.Path(__file__).resolve().parent.parent
MARK = "<!--deep-->"
ST = 'style="font-size:17px;line-height:1.7;margin-bottom:9px"'


def block(d):
    o = [MARK, '      <h2>Por que isso importa</h2>']
    for p in d["why"]:
        o.append(f"\n      <p>{p}</p>")
    if d.get("numeros"):
        o.append('\n      <h2>Os números, passo a passo</h2>\n\n      <ul style="margin:0 0 20px;padding-left:22px">')
        o += [f"        <li {ST}>{x}</li>" for x in d["numeros"]]
        o.append("      </ul>")
    o.append('\n      <h2>Perguntas frequentes</h2>')
    for q, a in d["faq"]:
        o.append(f"\n      <p><b>{q}</b><br>{a}</p>")
    if d.get("leia"):
        o.append('\n      <h2>Fontes primárias e leitura adicional</h2>\n\n      <ul style="margin:0 0 20px;padding-left:22px">')
        o += [f'        <li {ST}><a href="{u}" target="_blank" rel="noopener">{l}</a></li>' for l, u in d["leia"]]
        o.append("      </ul>")
    return "\n".join(o) + "\n\n      "


def load():
    D = {}
    for f in sorted(glob.glob(str(ROOT / "tools" / "aprof" / "*.py"))):
        sp = importlib.util.spec_from_file_location("m", f)
        m = importlib.util.module_from_spec(sp)
        sp.loader.exec_module(m)
        D.update(m.D)
    return D


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    dry = "--dry-run" in sys.argv
    for slug, d in load().items():
        f = ROOT / f"{slug}.html"
        t = f.read_text(encoding="utf-8")
        if MARK in t:
            print(slug, "ja tem")
            continue
        if t.count("<!--ctx-->") != 1:
            print(slug, "ancora ctx:", t.count("<!--ctx-->"))
            continue
        t = t.replace("<!--ctx-->", block(d) + "<!--ctx-->", 1)
        if not dry:
            f.write_text(t, encoding="utf-8")
        print(slug, "ok")
