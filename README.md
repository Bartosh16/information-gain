# information-gain

Skill dla Claude Code (i innych agentów), który mówi, **co dodać do artykułu**, żeby wnosił coś, czego nie ma w topie Google.

Podajesz frazę i – jeśli już masz – swój tekst. Dostajesz listę w trzech koszykach:

- **łatwe** – zrobisz w kilka godzin, często z pomocą AI,
- **drogie, ale warto** – dni albo tygodnie pracy, ale konkurencja tego nie skopiuje,
- **nie warto** – nie pasuje do tego typu treści albo koszt się nie zwróci.

Do tego **bilet wejścia**: tezy, które ma większość topu, a Tobie ich brakuje.

## Jak to działa

1. **Query fan-out** – agent rozpisuje frazę na 10–15 zapytań pobocznych.
2. **SERP** – top 10 dla każdego zapytania z Twojego SERP API.
3. **Ranking URL-i** – które strony wracają w topach wielu zapytań. Te czytelnik zobaczy na pewno.
4. **Pobranie treści** – pełny tekst, razem z FAQ i akordeonami, które zwykłe ekstraktory gubią.
5. **Analiza** – co mają wszyscy (konsensus), co ma jeden (unikat), czego nie ma nikt (luki z fan-outu i brakujące elementy).
6. **27 źródeł information gain** – ocena 0–1–2 każdej strony i Twojego tekstu.
7. **Matryca decyzyjna** – typ treści × koszt × fosa × Twoje zasoby → koszyki.
8. **Sugestie** – konkretne rzeczy do dodania: co, gdzie w tekście, kto to zrobi i ile to zajmie.

Liczenie (ranking, konsensus, koszyki) robią skrypty, więc wynik da się powtórzyć. Czytanie stron, nadawanie kluczy tezom i ocenę elementów robi model, z dowodem przy każdej ocenie.

## Instalacja

### Claude Code – jako plugin

```
/plugin marketplace add Bartosh16/information-gain
/plugin install information-gain@information-gain
```

### Claude Code – ręcznie

Skopiuj katalog `skills/ig-sugestie` do `~/.claude/skills/` (dla wszystkich projektów) albo do `.claude/skills/` w projekcie.

### Codex, Cursor i inne agenty

Sklonuj repo i otwórz je w agencie. Plik `AGENTS.md` kieruje agenta do instrukcji skilla. Możesz też napisać wprost: „Przeczytaj `skills/ig-sugestie/SKILL.md` i wykonaj dla frazy …”.

### Python

Python 3.10 lub nowszy:

```
pip install -r skills/ig-sugestie/requirements.txt
```

## Klucz API

Wystarczy jeden dostawca. Ustaw zmienną środowiskową albo wpisz ją do pliku `.env` w katalogu, z którego uruchamiasz agenta (wzór: `.env.example`).

| Dostawca | Zmienne | Wyniki |
|---|---|---|
| [SerpAPI](https://serpapi.com) | `SERPAPI_API_KEY` | Google |
| [DataForSEO](https://dataforseo.com) | `DATAFORSEO_LOGIN`, `DATAFORSEO_PASSWORD` | Google, domyślnie Polska (`DATAFORSEO_LOCATION_CODE=2616`) |
| [Serpdata.io](https://serpdata.io) | `SERPDATA_API_KEY` | Google |
| [Brave Search API](https://brave.com/search/api/) | `BRAVE_API_KEY` | własny indeks Brave, kolejność inna niż w Google |

Sprawdzenie: `python skills/ig-sugestie/scripts/serp.py --check`. Jeden przebieg to 11–16 zapytań do API.

## Użycie

W Claude Code (po instalacji ręcznej `/ig-sugestie`, jako plugin `/information-gain:ig-sugestie`):

```
/ig-sugestie fraza: ubezpieczenie przyczepki, artykuł: teksty/przyczepka.md
```

albo zwyczajnie: „Co dodać do mojego artykułu o ubezpieczeniu przyczepki, żeby miał information gain?”. Bez artykułu skill działa w trybie planowania i podpowiada, co powinno się znaleźć w tekście, który dopiero powstanie.

Skill zapyta raz, czym dysponujesz (własne dane, dostęp do klientów, praktyka, ekspert, czas, nagrania), bo od tego zależy, co jest dla Ciebie łatwe, a co drogie. Wynik ląduje w `ig-[fraza]/sugestie.md`, obok wszystkie pliki pośrednie.

## Czego skill nie robi

- **Nie pisze za Ciebie.** Mówi, co dodać. Danych, cytatów ani doświadczeń nie zmyśla, a cztery elementy (doświadczenie autora, dowód użycia, historia porażki, wystąpienie) zawsze zostawia Tobie.
- **Nie obiecuje pozycji.** Information gain to patent Google [US11354342B2](https://patents.google.com/patent/US11354342B2) – ocena, ile nowego wnosi dokument względem tego, co użytkownik już widział. Google nie potwierdził, że to sygnał rankingowy. Skill pomaga pisać teksty, które wnoszą coś nowego, bo to ma sens niezależnie od patentu.
- **Matryca to ocena ekspercka, nie pomiar.** Uzasadnienia są w `skills/ig-sugestie/references/elementy-27.md`. Nie zgadzasz się – zmień `scripts/elementy.py` i wygeneruj plik od nowa.

## Status

Wersja 1.0. Ranking, pobieranie treści, konsensus i koszyki przetestowane na prawdziwych danych z SERP-a. Integracje Brave i Serpdata.io pochodzą z narzędzia używanego w produkcji, a SerpAPI i DataForSEO są napisane według oficjalnej dokumentacji. Coś nie działa? Zgłoś to w Issues.

## Autor

Daniel Bartosiewicz, [DBest Content](https://dbest-content.com). Powstało na Festiwal SEO 2026.

Licencja MIT.
