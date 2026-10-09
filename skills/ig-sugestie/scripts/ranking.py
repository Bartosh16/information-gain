# -*- coding: utf-8 -*-
"""
Ranking URL-i z fan-outu: ile razy ten sam adres wraca w topach różnych zapytań.

Punkty: za każde wystąpienie 11 − pozycja (1. miejsce = 10 pkt). URL, który siedzi
w topie wielu zapytań pobocznych, to strona, którą czytelnik zobaczy na pewno – z nią
porównujesz swój tekst.

Wejście: serp.json ze scripts/serp.py.
Wyjście: ranking.json i ranking.md obok wejścia.

Uruchom:  python scripts/ranking.py ig-fraza/serp.json --wyklucz mojadomena.pl
"""
import argparse
import json
import sys
from pathlib import Path
from urllib.parse import urlparse

# Adresy, które rzadko są artykułem do porównania. Tylko flaga: decyzję podejmuje model.
NIE_ARTYKUL = ("youtube.com", "youtu.be", "facebook.com", "instagram.com", "linkedin.com", "tiktok.com",
               "x.com", "twitter.com", "pinterest.", "reddit.com", "wykop.pl", "quora.com", "linguee.",
               "studocu.com", "allegro.pl", "amazon.", "ceneo.pl", "google.com/maps")


def domena(url):
    d = urlparse(url).netloc.lower()
    return d[4:] if d.startswith("www.") else d


def norm(url):
    p = urlparse(url)
    return f"{domena(url)}{p.path.rstrip('/')}".lower()


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("serp")
    ap.add_argument("--wyklucz", nargs="*", default=[], help="domeny do pominięcia, np. własna")
    a = ap.parse_args()

    src = Path(a.serp)
    serp = json.loads(src.read_text(encoding="utf-8"))
    wyklucz = {w.lower().removeprefix("www.") for w in a.wyklucz}
    stat = {}
    for q, wyniki in serp.items():
        for w in wyniki:
            url = w.get("url")
            if not url:
                continue
            k = norm(url)
            s = stat.setdefault(k, {"url": url, "domena": domena(url), "title": w.get("title", ""),
                                    "wystapienia": 0, "punkty": 0, "pozycje": [], "zapytania": []})
            if q in s["zapytania"]:
                continue
            s["wystapienia"] += 1
            s["punkty"] += max(0, 11 - int(w.get("position", 10)))
            s["pozycje"].append(int(w.get("position", 10)))
            s["zapytania"].append(q)

    lista = []
    for s in stat.values():
        s["srednia_pozycja"] = round(sum(s["pozycje"]) / len(s["pozycje"]), 1)
        s["udzial"] = round(s["wystapienia"] / max(1, len(serp)), 2)
        s["wykluczony"] = any(s["domena"] == w or s["domena"].endswith("." + w) for w in wyklucz)
        s["flaga"] = "nie-artykuł?" if any(x in s["url"].lower() for x in NIE_ARTYKUL) else ""
        lista.append(s)
    lista.sort(key=lambda s: (-s["punkty"], -s["wystapienia"], s["srednia_pozycja"]))

    out = src.parent
    (out / "ranking.json").write_text(json.dumps(lista, ensure_ascii=False, indent=2), encoding="utf-8")
    w = ["# Ranking URL-i z fan-outu", "", f"Zapytań: {len(serp)}. Unikalnych URL-i: {len(lista)}.", "",
         "| # | URL | Wystąpienia | Punkty | Śr. pozycja | Uwagi |", "|---|---|---|---|---|---|"]
    for i, s in enumerate(lista[:30], 1):
        uw = ", ".join(x for x in (s["flaga"], "wykluczony" if s["wykluczony"] else "") if x)
        w.append(f"| {i} | {s['url']} | {s['wystapienia']}/{len(serp)} | {s['punkty']} | {s['srednia_pozycja']} | {uw} |")
    (out / "ranking.md").write_text("\n".join(w) + "\n", encoding="utf-8")

    print(f"{len(serp)} zapytań, {len(lista)} URL-i. Top 10:")
    for s in lista[:10]:
        print(f"  {s['punkty']:4d} pkt | {s['wystapienia']:2d}x | poz. {s['srednia_pozycja']:4} | {s['url'][:80]} {s['flaga']}")
    print(out / "ranking.md")


if __name__ == "__main__":
    main()
