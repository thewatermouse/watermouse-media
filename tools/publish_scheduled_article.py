# -*- coding: utf-8 -*-
"""Publica uma materia agendada a partir de um spec em rascunhos/ (gera, commit, push e confere se entrou no ar).

Uso (na raiz do repo): python -I tools/publish_scheduled_article.py rascunhos/AAAA-MM-DD-slug.json
Pensado pra rodar em tarefa agendada de uma materia JA APROVADA pelo Rodrigo. Seguro pra rodar duas vezes:
se o arquivo da materia ja existir, nao faz nada."""
import datetime as dt
import json
import pathlib
import subprocess
import sys
import time
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = "https://media.thewatermouse.com"


def git(*a, check=True):
    return subprocess.run(["git", *a], cwd=ROOT, check=check, capture_output=True, text=True, encoding="utf-8")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    spec_path = ROOT / sys.argv[1]
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    slug, cat = spec["slug"], spec["cat"]
    if not (ROOT / f"{slug}.html").exists():  # data de publicacao = momento real (spec pode ter sido antecipado na programacao)
        now = dt.datetime.now(dt.timezone(dt.timedelta(hours=-3))).replace(microsecond=0)
        spec["date_iso"] = now.isoformat()
        spec_path.write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding="utf-8")
    if (ROOT / f"{slug}.html").exists():
        print(f"{slug}.html ja existe: nada a fazer (materia ja publicada ou gerada).")
        return
    assert (ROOT / spec["image"]).exists(), f"imagem ausente: {spec['image']}"
    subprocess.run([sys.executable, "-I", str(ROOT / "tools" / "build_article.py"), str(spec_path)], cwd=ROOT, check=True)
    files = [f"{slug}.html", spec["image"], "index.html", f"{cat}.html", "sitemap.xml", "feed.xml", "links/index.html"]
    git("add", *files)
    msg = (f"Nova matéria: {spec['title']}\n\nPublicada por tarefa agendada (spec aprovado pelo Rodrigo).\n\n"
           "Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>")
    git("commit", "-q", "-m", msg)
    r = git("push", check=False)
    if r.returncode != 0:
        git("pull", "--rebase", "-q", check=False)
        r = git("push", check=False)
    print("push:", "ok" if r.returncode == 0 else "FALHOU: " + r.stderr[-300:])
    if r.returncode != 0:
        sys.exit(1)
    try:  # vitrine da raiz (best-effort: falha aqui nao invalida a publicacao)
        subprocess.run([sys.executable, "-I", str(ROOT / "tools" / "update_home_latest.py"), "--push"], cwd=ROOT, timeout=120)
    except Exception as e:
        print("home nao atualizada:", e)
    url = f"{BASE}/{slug}.html"
    for _ in range(30):
        try:
            if urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "wm-check"}), timeout=20).status == 200:
                print("NO AR:", url)
                return
        except Exception:
            pass
        time.sleep(10)
    print("push feito, mas a pagina ainda nao respondeu 200 (pode ser so o deploy do GitHub Pages):", url)


if __name__ == "__main__":
    main()
