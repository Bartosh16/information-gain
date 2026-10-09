---
name: ig-sugestie
description: >-
  Sugestie information gain dla artykułu: query fan-out, top 10 z SERP API (SerpAPI, DataForSEO,
  Serpdata.io albo Brave), ranking URL-i, analiza „co mają wszyscy, co ma jeden, czego nie ma nikt”,
  a na końcu lista, co dodać do tekstu według 27 źródeł information gain i matrycy decyzyjnej:
  łatwe, drogie ale warto, nie warto. Używaj, gdy ktoś pisze „co dodać do artykułu”, „information
  gain dla frazy X”, „czym wyróżnić tekst na tle topu”, „luki w SERP”, „ig-sugestie” albo podaje
  frazę lub artykuł i pyta, jak go uczynić bardziej unikalnym niż konkurencja.
---

# Sugestie information gain

Wynik: lista konkretnych rzeczy do dodania do artykułu, podzielona na trzy koszyki – **łatwe**, **drogie, ale warto**, **nie warto** – plus bilet wejścia, czyli to, czego czytelnik oczekuje, bo ma to cały top.

Skill niczego nie dopisuje do artykułu. Mówi, co dopisać, gdzie, kto to zrobi i ile to kosztuje.

Ścieżki `scripts/` i `references/` są względem katalogu tego skilla. Wszystkie pliki robocze trafiają do `ig-[slug-frazy]/` w bieżącym katalogu.

## Zasady, których nie łamiesz

1. **Nie zmyślasz.** Żadnych liczb, cytatów, nazwisk, wyników testów ani doświadczeń. Sugestia mówi, co autor ma dostarczyć, a nie podaje gotowej treści, której nie da się sprawdzić.
2. **Elementy „tylko Ty”** (doświadczenie autora, dowód użycia, historia porażki, wystąpienie) zawsze opisujesz jako zadanie dla autora. Wersja wygenerowana przez AI to fałszerstwo, nie information gain.
3. **Punkt za to, co tekst robi, nie za to, co radzi.** Strona, która pisze „warto dodać dane z GUS”, a sama ich nie ma, dostaje 0.
4. **Nie powtarzasz mitów o patencie.** Information gain to patent Google US11354342B2 (zgłoszony 2018, udzielony 2022): ocena, ile nowego wnosi dokument względem tego, co użytkownik już widział. Google nie potwierdził, że to sygnał rankingowy, i nie publikuje progów „unikalnych encji”. Nie obiecuj pozycji.
5. **Strona bez treści to nie strona bez information gain.** Paywall, blokada albo słownik – pomijasz w ocenie i piszesz to w raporcie.

## Proces

### 0. Wejście

Ustal, a czego brakuje, przyjmij domyślnie i zapisz założenie (nie pytaj o każdy punkt):

- **fraza główna** – wymagana,
- **artykuł** – plik, URL, wklejony tekst albo brak (wtedy tryb planowania: sugestie do tekstu, który dopiero powstanie),
- **rynek** – domyślnie `pl`/`pl`,
- **typ treści** – jeden z: `evergreen`, `biezacy`, `ymyl`, `oferta`, `definicja`, `skala` (opisy w `references/elementy-27.md`, sekcja „Matryca”). Ustal sam z frazy i artykułu, YMYL ma pierwszeństwo,
- **zasoby autora** – zapytaj jednym pytaniem, co ma: `dane`, `klienci`, `praktyka`, `ekspert`, `czas`, `nagrania`. Brak odpowiedzi = `null` (koszt liczony jak bez zasobów, sugestie dostają „wymaga: …”).

Jeśli autor podał domenę swojej strony, zapamiętaj ją do `--wyklucz`.

### 1. Klucz do SERP API

```
python scripts/serp.py --check
```

Brak klucza – zatrzymaj się i powiedz, którą zmienną ustawić (README, sekcja „Klucz API”). Nie szukaj kluczy w plikach na dysku.

### 2. Query fan-out

Według `references/fan-out.md` rozpisz frazę na 10–15 zapytań pobocznych. Zapisz `ig-[slug]/fanout.json`.

### 3. SERP

```
python scripts/serp.py ig-[slug]/fanout.json --out ig-[slug]/serp.json --kraj pl --jezyk pl
```

### 4. Ranking URL-i

```
python scripts/ranking.py ig-[slug]/serp.json --wyklucz [domena-autora]
```

Przejrzyj `ranking.md`. Flaga „nie-artykuł?” to tylko podpowiedź: wideo, forum i sklep nie są tekstem do porównania, ale jeśli zajmują top, zapisz to jako sygnał intencji (ludzie chcą obejrzeć, zapytać albo kupić).

### 5. Pobranie treści

```
python scripts/pobierz.py ig-[slug]/ranking.json --top 10
```

Artykuł autora podany jako URL: `python scripts/pobierz.py --url [url] --nazwa artykul --out ig-[slug]/teksty`. Plik albo wklejony tekst zapisz jako `ig-[slug]/teksty/artykul.md`.

Sprawdź `teksty/indeks.json`. Strony z uwagą „mało treści” albo z błędem HTTP wyłącz z oceny. Do porównania wystarczy 6–10 stron merytorycznych.

### 6. Analiza: co mają wszyscy, co ma jeden, czego nie ma nikt

Przeczytaj każdą stronę w całości. Dla każdej wypisz tezy merytoryczne i nadaj im **klucze**: ta sama myśl u różnych autorów dostaje ten sam klucz, niezależnie od słów (`DEF_SESJA`, `KOSZT_OD_100ZL`). Zrób to samo dla artykułu autora. Zapisz `ig-[slug]/tezy.json` (format w nagłówku skryptu) i policz:

```
python scripts/konsensus.py ig-[slug]/tezy.json
```

„Czego nie ma nikt” ustalasz sam z dwóch źródeł:

- **luki z fan-outu** – zapytania z `fanout.json`, na które żadna pobrana strona nie odpowiada wprost,
- **luki w elementach** – wynik kroku 7 (elementy, których w topie nikt nie robi).

### 7. Ocena 27 elementów

Według `references/elementy-27.md` oceń każdą stronę i artykuł: 0, 1 albo 2 punkty na element, z krótkim dowodem (cytat albo miejsce w tekście). Bez dowodu nie ma punktu. Grafiki sprawdź w `indeks.json` (pole `grafiki`) i w tekście. Zapisz `ig-[slug]/ocena.json` razem z typem treści i zasobami, potem:

```
python scripts/koszyki.py ig-[slug]/ocena.json
```

### 8. Sugestie

`koszyki.md` mówi, które elementy wchodzą do którego koszyka. Twoja robota to zamienić element w **konkretną rzecz w tym temacie**:

- weź z koszyka „łatwe” do 5 pozycji, z „drogie, ale warto” do 3 – najpierw te, których w topie nie robi nikt, i te, które zamykają lukę z fan-outu,
- przy każdej podaj: co dokładnie dodać, gdzie w artykule (istniejąca sekcja albo nowa), dlaczego (luka z fan-outu, nikt w topie, ślad do dociągnięcia), kto to zrobi i ile to zajmie,
- przy YMYL dopisz ryzyko: źródło pierwotne obowiązkowe, kalkulator wymaga testów, case wymaga zgody,
- koszyk „nie warto” – po jednym zdaniu powodu, bez rozpisywania,
- możesz przesunąć element między koszykami, jeśli znasz powód, którego skrypt nie widzi (np. autor ma gotowe nagranie). Każdą korektę wpisz w „Jak to policzone”.

Raport według `references/szablon-raportu.md`, zapis do `ig-[slug]/sugestie.md`. W odpowiedzi pokaż koszyki i podaj ścieżkę do pliku.

## Pliki w `ig-[slug]/`

| Plik | Kto tworzy |
|---|---|
| `fanout.json` | model |
| `serp.json` | `serp.py` |
| `ranking.json`, `ranking.md` | `ranking.py` |
| `teksty/*.md`, `teksty/indeks.json` | `pobierz.py` |
| `tezy.json` | model |
| `konsensus.json`, `konsensus.md` | `konsensus.py` |
| `ocena.json` | model |
| `koszyki.json`, `koszyki.md` | `koszyki.py` |
| `sugestie.md` | model, wynik końcowy |
