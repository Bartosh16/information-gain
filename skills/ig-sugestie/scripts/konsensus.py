# -*- coding: utf-8 -*-
"""
Trójpodział tez: co mają wszyscy (konsensus), co ma jeden (unikat), a do tego –
gdy jest artykuł – czego brakuje Tobie i co masz tylko Ty.

Klucze tez nadaje model (ta sama myśl u różnych autorów = ten sam klucz, niezależnie
od słów). Kod tylko liczy. Porównanie słów nie łapie parafrazy, dlatego klucze.

Wejście: tezy.json
{
  "opisy":   {"klucz": "jednozdaniowy opis tezy", ...},
  "strony":  {"01": {"url": "...", "tezy": ["klucz", ...]}, ...},
  "artykul": ["klucz", ...]          # opcjonalnie
}
Konsensus: teza na co najmniej max(2, ceil(35% stron)) stronach (8 stron -> 3).

Wyjście: konsensus.json i konsensus.md obok wejścia.

Uruchom:  python scripts/konsensus.py ig-fraza/tezy.json
"""
import json
import math
import sys
from collections import defaultdict
from pathlib import Path


def policz(d):
    strony = d["strony"]
    n = len(strony)
    prog = max(2, math.ceil(0.35 * n))
    gdzie = defaultdict(set)
    for sid, s in strony.items():
        for t in set(s["tezy"]):
            gdzie[t].add(sid)
    kons = sorted((t for t, s in gdzie.items() if len(s) >= prog), key=lambda t: -len(gdzie[t]))
    unik = {sid: sorted(t for t in set(s["tezy"]) if len(gdzie[t]) == 1) for sid, s in strony.items()}
    out = {"stron": n, "prog_konsensusu": prog,
           "konsensus": [{"teza": t, "stron": len(gdzie[t]), "gdzie": sorted(gdzie[t])} for t in kons],
           "unikaty": unik}
    art = d.get("artykul")
    if art is not None:
        art = set(art)
        out["artykul"] = {
            "brak_konsensusu": [t for t in kons if t not in art],
            "tylko_ty": sorted(t for t in art if t not in gdzie),
            "powielone": sorted(t for t in art if t in gdzie),
            "pokrycie_konsensusu": round(sum(t in art for t in kons) / len(kons), 2) if kons else None,
        }
    return out


def md(w, opisy, strony):
    o = lambda t: f"{t} – {opisy.get(t, '')}".rstrip(" –")  # noqa: E731
    r = ["# Co mają wszyscy, co ma jeden, czego brakuje", "",
         f"Stron: {w['stron']}. Konsensus od {w['prog_konsensusu']} stron.", "",
         f"## Konsensus ({len(w['konsensus'])})", ""]
    r += [f"- {o(k['teza'])} ({k['stron']}/{w['stron']})," for k in w["konsensus"]] or ["Brak."]
    r += ["", "## Unikaty stron", ""]
    for sid, ts in w["unikaty"].items():
        r.append(f"- **{sid}** {strony[sid].get('url', '')}: {len(ts)}" + (f" – {', '.join(ts)}" if ts else ""))
    if "artykul" in w:
        a = w["artykul"]
        r += ["", "## Twój artykuł", "",
              f"Pokrycie konsensusu: {a['pokrycie_konsensusu']}.", "",
              f"### Brakuje Ci konsensusu – bilet wejścia ({len(a['brak_konsensusu'])})", ""]
        r += [f"- {o(t)}," for t in a["brak_konsensusu"]] or ["Brak."]
        r += ["", f"### Masz tylko Ty – to już jest information gain ({len(a['tylko_ty'])})", ""]
        r += [f"- {o(t)}," for t in a["tylko_ty"]] or ["Brak."]
    return "\n".join(r) + "\n"


def main():
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    src = Path(sys.argv[1])
    d = json.loads(src.read_text(encoding="utf-8"))
    w = policz(d)
    (src.parent / "konsensus.json").write_text(json.dumps(w, ensure_ascii=False, indent=2), encoding="utf-8")
    (src.parent / "konsensus.md").write_text(md(w, d.get("opisy", {}), d["strony"]), encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    print(f"konsensus: {len(w['konsensus'])} tez (próg {w['prog_konsensusu']}/{w['stron']}), "
          f"unikaty: {sum(len(v) for v in w['unikaty'].values())}")
    if "artykul" in w:
        print(f"artykuł: brak konsensusu {len(w['artykul']['brak_konsensusu'])}, tylko Ty {len(w['artykul']['tylko_ty'])}")
    print(src.parent / "konsensus.md")


if __name__ == "__main__":
    main()
