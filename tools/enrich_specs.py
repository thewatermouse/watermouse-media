"""Insere 'Para entender o contexto' + 'Termos uteis' no body_html dos specs agendados em rascunhos/ (idempotente).

Uso: python -I tools/enrich_specs.py [--dry-run]"""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from enrich import MARK, block
from enrich_specs_a import S as A
from enrich_specs_b import S as B

ROOT = pathlib.Path(__file__).resolve().parent.parent
S = {**A, **B}

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    dry = "--dry-run" in sys.argv
    n = 0
    for f in sorted((ROOT / "rascunhos").glob("*.json")):
        if f.stem not in S:
            continue
        spec = json.loads(f.read_text(encoding="utf-8"))
        body = spec["body_html"]
        if MARK in body:
            continue
        anchor = "<h2>As ressalvas</h2>"
        blk = block(*S[f.stem]).rstrip() + "\n\n      "
        if body.count(anchor) == 1:
            body = body.replace(anchor, blk + anchor, 1)
        else:
            body = body.rstrip() + "\n\n      " + blk.rstrip() + "\n"
        spec["body_html"] = body
        if not dry:
            f.write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding="utf-8")
        n += 1
    missing = [k for k in S if not (ROOT / "rascunhos" / f"{k}.json").exists()]
    print("enriquecidos:", n, "| chaves sem spec:", missing)
