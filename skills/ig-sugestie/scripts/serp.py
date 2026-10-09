# -*- coding: utf-8 -*-
"""
Pobiera top 10 dla każdego zapytania z fan-outu. Jeden z czterech dostawców:

    SerpAPI      SERPAPI_API_KEY                      (Google)
    DataForSEO   DATAFORSEO_LOGIN + DATAFORSEO_PASSWORD (Google)
    Serpdata.io  SERPDATA_API_KEY                     (Google)
    Brave Search BRAVE_API_KEY                        (własny indeks Brave, nie Google)

Bez --dostawca wybiera pierwszego z kluczem, w tej kolejności. Klucze bierze ze zmiennych
środowiskowych albo z pliku .env w bieżącym katalogu (jeśli jest python-dotenv).

Wejście: fanout.json – {"fraza": "...", "zapytania": ["...", {"q": "...", "typ": "..."}]}
         albo plik .txt z jednym zapytaniem w linii.
Wyjście: serp.json – {"zapytanie": [{"url", "title", "description", "position"}, ...]}

Uruchom:  python scripts/serp.py --check
          python scripts/serp.py ig-fraza/fanout.json --out ig-fraza/serp.json
"""
import argparse
import json
import os
import sys
import time
from pathlib import Path

import httpx

try:
    from dotenv import load_dotenv
    load_dotenv(Path.cwd() / ".env")
except ImportError:
    pass

TOP = 10
KOLEJNOSC = ["serpapi", "dataforseo", "serpdata", "brave"]


def klucz(d):
    if d == "serpapi":
        return os.getenv("SERPAPI_API_KEY")
    if d == "dataforseo":
        return os.getenv("DATAFORSEO_LOGIN") and os.getenv("DATAFORSEO_PASSWORD")
    if d == "serpdata":
        return os.getenv("SERPDATA_API_KEY")
    if d == "brave":
        return os.getenv("BRAVE_API_KEY")


def wynik(url, title, desc, pos):
    return {"url": (url or "").rstrip("/"), "title": title or "", "description": desc or "", "position": pos}


def serpapi(q, kraj, jezyk):
    r = httpx.get("https://serpapi.com/search.json",
                  params={"engine": "google", "q": q, "api_key": os.getenv("SERPAPI_API_KEY"),
                          "gl": kraj.lower(), "hl": jezyk, "google_domain": os.getenv("SERPAPI_GOOGLE_DOMAIN", f"google.{kraj.lower()}")},
                  timeout=30)
    r.raise_for_status()
    org = r.json().get("organic_results", [])
    return [wynik(i.get("link"), i.get("title"), i.get("snippet"), n) for n, i in enumerate(org[:TOP], 1) if i.get("link")]


def dataforseo(q, kraj, jezyk):
    # location_code: 2000 + numeryczny kod ISO kraju (2616 = Polska, 2840 = USA).
    # Inny kraj: DATAFORSEO_LOCATION_CODE, lista w /v3/serp/google/locations
    loc = int(os.getenv("DATAFORSEO_LOCATION_CODE", "2616"))
    r = httpx.post("https://api.dataforseo.com/v3/serp/google/organic/live/regular",
                   auth=(os.getenv("DATAFORSEO_LOGIN"), os.getenv("DATAFORSEO_PASSWORD")),
                   json=[{"keyword": q, "location_code": loc, "language_code": jezyk, "depth": TOP}],
                   timeout=60)
    r.raise_for_status()
    zad = (r.json().get("tasks") or [{}])[0]
    if zad.get("status_code") not in (None, 20000):
        raise RuntimeError(f"DataForSEO: {zad.get('status_code')} {zad.get('status_message')}")
    items = ((zad.get("result") or [{}])[0] or {}).get("items") or []
    org = [i for i in items if i.get("type") == "organic"]
    return [wynik(i.get("url"), i.get("title"), i.get("description"), n) for n, i in enumerate(org[:TOP], 1)]


def serpdata(q, kraj, jezyk):
    r = httpx.get("https://api.serpdata.io/v1/search",
                  params={"q": q, "api_key": os.getenv("SERPDATA_API_KEY"), "num": TOP}, timeout=30)
    r.raise_for_status()
    org = r.json().get("organic_results", [])
    return [wynik(i.get("link"), i.get("title"), i.get("snippet"), n) for n, i in enumerate(org[:TOP], 1) if i.get("link")]


def brave(q, kraj, jezyk):
    h = {"Accept": "application/json", "Accept-Encoding": "gzip", "X-Subscription-Token": os.getenv("BRAVE_API_KEY")}
    p = {"q": q, "count": TOP, "country": kraj.upper(), "search_lang": jezyk}
    r = httpx.get("https://api.search.brave.com/res/v1/web/search", headers=h, params=p, timeout=30)
    if r.status_code == 422:  # kraj albo język spoza listy Brave – ponów bez nich
        r = httpx.get("https://api.search.brave.com/res/v1/web/search", headers=h, params={"q": q, "count": TOP}, timeout=30)
    r.raise_for_status()
    org = r.json().get("web", {}).get("results", [])
    return [wynik(i.get("url"), i.get("title"), i.get("description"), n) for n, i in enumerate(org[:TOP], 1) if i.get("url")]


DOSTAWCY = {"serpapi": serpapi, "dataforseo": dataforseo, "serpdata": serpdata, "brave": brave}


def wczytaj(p):
    p = Path(p)
    if p.suffix == ".json":
        d = json.loads(p.read_text(encoding="utf-8"))
        zap = [d["fraza"]] if d.get("fraza") else []
        zap += [z["q"] if isinstance(z, dict) else z for z in d.get("zapytania", [])]
    else:
        zap = p.read_text(encoding="utf-8").splitlines()
    out, seen = [], set()
    for z in zap:
        z = " ".join(str(z).split())
        if z and z.lower() not in seen:
            seen.add(z.lower())
            out.append(z)
    return out


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("wejscie", nargs="?")
    ap.add_argument("--out", default="serp.json")
    ap.add_argument("--dostawca", choices=KOLEJNOSC)
    ap.add_argument("--kraj", default="pl")
    ap.add_argument("--jezyk", default="pl")
    ap.add_argument("--max", type=int, default=20, help="maksymalna liczba zapytań (koszt API)")
    ap.add_argument("--przerwa", type=float, default=0.5)
    ap.add_argument("--check", action="store_true", help="pokaż, który dostawca ma klucz")
    a = ap.parse_args()

    dost = a.dostawca or next((d for d in KOLEJNOSC if klucz(d)), None)
    if a.check:
        for d in KOLEJNOSC:
            print(f"{d:11} {'klucz jest' if klucz(d) else 'brak klucza'}")
        print(f"użyty: {dost or 'żaden – ustaw jeden klucz, patrz README'}")
        return
    if not a.wejscie:
        ap.error("podaj plik z zapytaniami")
    if not dost or not klucz(dost):
        raise SystemExit("Brak klucza API. Ustaw SERPAPI_API_KEY, DATAFORSEO_LOGIN + DATAFORSEO_PASSWORD, "
                         "SERPDATA_API_KEY albo BRAVE_API_KEY (zmienna środowiskowa lub .env).")
    if dost == "brave":
        print("Uwaga: Brave ma własny indeks, kolejność różni się od Google.")

    zap = wczytaj(a.wejscie)[: a.max]
    wyniki, puste = {}, 0
    for n, q in enumerate(zap, 1):
        try:
            wyniki[q] = DOSTAWCY[dost](q, a.kraj, a.jezyk)
        except Exception as exc:  # jedno zapytanie nie może wywrócić całego przebiegu
            print(f"  [{n:02d}] BŁĄD {exc.__class__.__name__}: {exc}"[:200])
            wyniki[q] = []
        puste += not wyniki[q]
        print(f"  [{n:02d}/{len(zap)}] {len(wyniki[q]):2d} wyników | {q[:70]}")
        time.sleep(a.przerwa)

    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps(wyniki, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"{dost}: {len(zap)} zapytań, {puste} pustych -> {a.out}")
    if puste == len(zap):
        raise SystemExit("Wszystkie zapytania puste – sprawdź klucz i limit konta.")


if __name__ == "__main__":
    main()
