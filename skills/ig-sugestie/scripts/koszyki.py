# -*- coding: utf-8 -*-
"""
Rozkłada 27 elementów information gain na koszyki według matrycy decyzyjnej:
łatwe / drogie, ale warto / nie warto / bilet wejścia / już masz.

Wejście: ocena.json (ocenę 0–1–2 z dowodem robi model, według references/elementy-27.md)
{
  "typ": "evergreen",                     # klucz z elementy.TYPY
  "zasoby": ["dane", "praktyka"],         # klucze z elementy.ZASOBY; null = nie wiadomo
  "strony": {"01": {"url": "...", "oceny": {"dane_zastane": [2, "dowód"], ...}}, ...},
  "artykul": {"oceny": {...}}             # null, gdy artykułu jeszcze nie ma
}
Brakujący element = 0.

Wyjście: koszyki.json i koszyki.md obok pliku wejściowego.

Uruchom:  python scripts/koszyki.py ig-fraza/ocena.json
"""
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from elementy import AI, E, GRUPY, KOSZT, TYPY, ZASOBY, dopasowanie  # noqa: E402

FOSA_RANG = {"niska": 0, "średnia": 1, "wysoka": 2}


def wynik(oceny, kr):
    v = (oceny or {}).get(kr, 0)
    return int(v[0] if isinstance(v, (list, tuple)) else v)


def rozloz(dane):
    typ = dane["typ"]
    if typ not in TYPY:
        raise SystemExit(f"Nieznany typ treści: {typ}. Dozwolone: {', '.join(TYPY)}")
    zasoby = dane.get("zasoby")
    znane = zasoby is not None
    zasoby = set(zasoby or [])
    for z in zasoby:
        if z not in ZASOBY:
            raise SystemExit(f"Nieznany zasób: {z}. Dozwolone: {', '.join(ZASOBY)}")
    strony = dane.get("strony", {})
    n = len(strony)
    art = (dane.get("artykul") or {}).get("oceny")
    prog_bilet = max(2, math.ceil(n / 2))

    wyniki = []
    for kr, (g, nazwa, pelne, koszt, zasob, ai, prz) in E.items():
        sc = [wynik(s.get("oceny"), kr) for s in strony.values()]
        smax = max(sc, default=0)
        spelne = sum(1 for x in sc if x == 2)
        a = wynik(art, kr) if art is not None else 0
        fit = dopasowanie(kr, typ)
        fosa = GRUPY[g][1]
        brak_zasobu = bool(zasob) and zasob not in zasoby
        k_eff = min(3, koszt + (1 if brak_zasobu else 0))
        r = {"id": kr, "nazwa": nazwa, "grupa": GRUPY[g][0], "fosa": fosa, "dopasowanie": fit,
             "koszt": KOSZT[k_eff], "koszt_poziom": k_eff, "kto": ai, "wymaga": zasob,
             "brak_zasobu": brak_zasobu and znane, "zasob_nieznany": bool(zasob) and not znane,
             "serp_max": smax, "serp_pelne": spelne, "stron": n, "artykul": a, "przyklad": prz}

        if art is not None and a == 2:
            r["koszyk"], r["powod"] = "masz", "artykuł robi to w pełni"
        elif fit == "○":
            r["koszyk"], r["powod"] = "nie_warto", f"nie pasuje do typu treści „{TYPY[typ]}”"
        elif ai == "tylko_ty" and znane and brak_zasobu:
            r["koszyk"], r["powod"] = "nie_warto", f"wymaga zasobu „{zasob}”, którego nie masz, a AI tego uczciwie nie zrobi"
        elif fosa == "niska" and n and spelne >= prog_bilet:
            r["koszyk"], r["powod"] = "bilet", f"standard w topie ({spelne}/{n} stron robi to w pełni) – zrób, ale to nie przewaga"
        elif k_eff == 1 or (k_eff == 2 and fosa == "niska" and fit == "●"):
            r["koszyk"] = "latwe"
            r["powod"] = "nikt w topie tego nie robi" if smax == 0 else ("w topie tylko ślad" if smax == 1 else f"{spelne}/{n} stron robi to w pełni")
        elif fit == "●" and fosa != "niska":
            r["koszyk"] = "drogie"
            r["powod"] = ("nikt w topie tego nie robi" if smax == 0 else "w topie tylko ślad" if smax == 1
                          else f"{spelne}/{n} stron robi to w pełni") + f", fosa {fosa}"
        else:
            r["koszyk"] = "nie_warto"
            r["powod"] = (f"koszt „{KOSZT[k_eff]}” przy dopasowaniu ◐ się nie zwróci" if fit == "◐"
                          else f"koszt „{KOSZT[k_eff]}”, a konkurencja łatwo to skopiuje")
        wyniki.append(r)

    klucz = lambda r: (r["serp_max"], -FOSA_RANG[r["fosa"]], r["koszt_poziom"], r["artykul"])  # noqa: E731
    out = {k: sorted([r for r in wyniki if r["koszyk"] == k], key=klucz)
           for k in ("bilet", "latwe", "drogie", "nie_warto", "masz")}
    out["meta"] = {"typ": typ, "typ_nazwa": TYPY[typ], "zasoby": sorted(zasoby) if znane else None,
                   "stron": n, "artykul": art is not None}
    return out


def md(k):
    m = k["meta"]
    zas = ", ".join(m["zasoby"]) if m["zasoby"] is not None else "nie podano (koszt liczony jak bez zasobów)"
    w = ["# Koszyki information gain", "",
         f"Typ treści: {m['typ_nazwa']}. Zasoby: {zas}. Stron w analizie: {m['stron']}. Artykuł: {'tak' if m['artykul'] else 'brak, tryb planowania'}.", ""]
    naglowki = {"bilet": "Bilet wejścia (standard w topie, nie przewaga)", "latwe": "Łatwe – zrób od razu",
                "drogie": "Drogie, ale warto", "nie_warto": "Nie warto (przy tym typie treści i zasobach)", "masz": "Już masz"}
    for kosz, tytul in naglowki.items():
        rows = k[kosz]
        w += [f"## {tytul} ({len(rows)})", ""]
        if not rows:
            w += ["Brak.", ""]
            continue
        w += ["| Element | Grupa | W topie | Artykuł | Koszt | Kto | Dlaczego tu |", "|---|---|---|---|---|---|---|"]
        for r in rows:
            uw = f" (wymaga: {r['wymaga']})" if r["brak_zasobu"] or r["zasob_nieznany"] else ""
            w.append(f"| {r['nazwa']} | {r['grupa']} | max {r['serp_max']}, pełne {r['serp_pelne']}/{r['stron']} | {r['artykul']} | "
                     f"{r['koszt']}{uw} | {AI[r['kto']]} | {r['powod']} |")
        w.append("")
    return "\n".join(w)


def main():
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    src = Path(sys.argv[1])
    dane = json.loads(src.read_text(encoding="utf-8"))
    k = rozloz(dane)
    (src.parent / "koszyki.json").write_text(json.dumps(k, ensure_ascii=False, indent=2), encoding="utf-8")
    (src.parent / "koszyki.md").write_text(md(k), encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    print("  ".join(f"{x}: {len(k[x])}" for x in ("bilet", "latwe", "drogie", "nie_warto", "masz")))
    print(src.parent / "koszyki.md")


if __name__ == "__main__":
    main()
