# -*- coding: utf-8 -*-
"""
Pobiera pełną treść stron do porównania: trafilatura + to, co trafilatura gubi.

Trafilatura potrafi zgubić zwinięte FAQ i akordeony (zostają same pytania). Skrypt
dokleja więc z surowego HTML: FAQPage z JSON-LD, bloki <details> i elementy z „faq”
albo „accordion” w klasie lub id – o ile ich tekstu nie ma już w treści. Bez tego
analiza wykaże „lukę”, której w rzeczywistości nie ma.

Wejście: ranking.json (bierze top N bez wykluczonych i bez flagi „nie-artykuł?”)
         albo --url adres [adres ...].
Wyjście: katalog teksty/ z plikami NN-domena.md i teksty/indeks.json.

Uruchom:  python scripts/pobierz.py ig-fraza/ranking.json --top 10
          python scripts/pobierz.py --url https://mojastrona.pl/artykul --nazwa artykul --out ig-fraza/teksty
"""
import argparse
import json
import re
import sys
import time
from pathlib import Path
from urllib.parse import urlparse

import httpx
import trafilatura
from bs4 import BeautifulSoup

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36")
MIN_SLOW = 300


def czysc(t):
    return " ".join((t or "").split())


def faq_z_jsonld(soup):
    out = []

    def zbierz(o):
        if isinstance(o, list):
            for x in o:
                zbierz(x)
        elif isinstance(o, dict):
            if o.get("@type") == "Question":
                odp = o.get("acceptedAnswer") or {}
                if isinstance(odp, list):
                    odp = odp[0] if odp else {}
                tekst = BeautifulSoup(str(odp.get("text", "")), "html.parser").get_text(" ")
                out.append(f"**{czysc(o.get('name'))}** {czysc(tekst)}")
            for v in o.values():
                if isinstance(v, (dict, list)):
                    zbierz(v)

    for s in soup.find_all("script", type="application/ld+json"):
        try:
            zbierz(json.loads(s.string or ""))
        except (json.JSONDecodeError, TypeError):
            continue
    return out


def bloki_zwiniete(soup):
    out = []
    for el in soup.find_all("details"):
        out.append(czysc(el.get_text(" ")))
    wzor = re.compile(r"faq|accordion|akordeon", re.I)
    for el in soup.find_all(attrs={"class": wzor}) + soup.find_all(attrs={"id": wzor}):
        if el.find_parent(attrs={"class": wzor}):  # tylko najwyższy poziom
            continue
        out.append(czysc(el.get_text(" ")))
    return [b for b in out if len(b) > 40]


def wyciagnij(html, url):
    tekst = trafilatura.extract(html, url=url, output_format="markdown", include_tables=True,
                                include_comments=False, include_links=False, include_images=False,
                                favor_recall=True) or ""
    soup = BeautifulSoup(html, "html.parser")
    plaski = czysc(tekst).lower()
    dodatki = []
    for b in faq_z_jsonld(soup) + bloki_zwiniete(soup):
        probka = czysc(re.sub(r"\*\*", "", b))[-80:].lower()  # koniec bloku = odpowiedź
        if probka and probka not in plaski:
            dodatki.append(b)
            plaski += " " + czysc(re.sub(r"\*\*", "", b)).lower()
    if dodatki:
        tekst += "\n\n## Doklejone z surowego HTML (FAQ, akordeony)\n\n" + "\n\n".join(dodatki)
    obrazy = len(soup.select("article img, main img, article svg, main svg"))
    return tekst.strip(), len(dodatki), obrazy


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("ranking", nargs="?")
    ap.add_argument("--top", type=int, default=10)
    ap.add_argument("--url", nargs="*", default=[])
    ap.add_argument("--nazwa", help="nazwa pliku dla pojedynczego --url, np. artykul")
    ap.add_argument("--out", help="katalog wyjściowy (domyślnie teksty/ obok ranking.json)")
    ap.add_argument("--przerwa", type=float, default=1.0)
    a = ap.parse_args()

    if a.ranking:
        lista = json.loads(Path(a.ranking).read_text(encoding="utf-8"))
        cele = [s["url"] for s in lista if not s.get("wykluczony") and not s.get("flaga")][: a.top]
        out = Path(a.out) if a.out else Path(a.ranking).parent / "teksty"
    elif a.url:
        cele = a.url
        out = Path(a.out or "teksty")
    else:
        ap.error("podaj ranking.json albo --url")
    out.mkdir(parents=True, exist_ok=True)

    indeks_p = out / "indeks.json"
    indeks = json.loads(indeks_p.read_text(encoding="utf-8")) if indeks_p.exists() else []
    with httpx.Client(follow_redirects=True, headers={"User-Agent": UA, "Accept-Language": "pl,en;q=0.8"}, timeout=25) as c:
        for n, url in enumerate(cele, 1):
            dom = urlparse(url).netloc.removeprefix("www.")
            nazwa = a.nazwa if (a.nazwa and len(cele) == 1) else f"{n:02d}-{re.sub(r'[^a-z0-9.-]', '-', dom.lower())}"
            wpis = {"plik": f"{nazwa}.md", "url": url, "status": None, "slow": 0, "doklejone": 0, "grafiki": 0, "uwaga": ""}
            try:
                r = c.get(url)
                wpis["status"] = r.status_code
                if r.status_code >= 400:
                    wpis["uwaga"] = f"HTTP {r.status_code} – nie oceniaj tej strony"
                else:
                    tekst, dokl, img = wyciagnij(r.text, str(r.url))
                    wpis.update(slow=len(tekst.split()), doklejone=dokl, grafiki=img)
                    if wpis["slow"] < MIN_SLOW:
                        wpis["uwaga"] = "mało treści: blokada, paywall albo nie artykuł – sprawdź, zanim ocenisz"
                    (out / wpis["plik"]).write_text(f"<!-- {url} -->\n# {dom}\n\n{tekst}\n", encoding="utf-8")
            except httpx.HTTPError as exc:
                wpis["uwaga"] = f"błąd pobrania: {exc.__class__.__name__}"
            indeks = [x for x in indeks if x["plik"] != wpis["plik"]] + [wpis]
            print(f"  [{n:02d}/{len(cele)}] {wpis['status']} {wpis['slow']:5d} słów  +{wpis['doklejone']} FAQ  {url[:70]}  {wpis['uwaga']}")
            time.sleep(a.przerwa)

    indeks_p.write_text(json.dumps(indeks, ensure_ascii=False, indent=2), encoding="utf-8")
    print(out)


if __name__ == "__main__":
    main()
