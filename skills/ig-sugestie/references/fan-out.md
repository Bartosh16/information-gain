# Query fan-out – jak rozpisać frazę na zapytania poboczne

Cel: zobaczyć temat tak, jak widzi go czytelnik, który szuka dalej. Strony, które wracają w topach wielu zapytań pobocznych, czytelnik przeczyta na pewno. Z nimi porównujesz artykuł.

## Zasady

- 10–15 zapytań plus fraza główna. Więcej podnosi koszt API, a mało dokłada.
- Każde zapytanie zachowuje główną encję frazy. „ubezpieczenie przyczepki” → „ile kosztuje ubezpieczenie przyczepki”, a nie „ile kosztuje OC”.
- Pisz w języku i formie, w jakiej ludzie wpisują zapytania: bez znaków zapytania, małymi literami, potocznie, z literówkami tylko wtedy, gdy są masowe.
- Bez duplikatów różniących się jednym słowem.

## Typy zapytań (pokryj co najmniej 6)

| Typ | Przykład dla „ubezpieczenie przyczepki” |
|---|---|
| definicja | czy przyczepka musi mieć OC |
| jak | jak ubezpieczyć przyczepkę lekką |
| koszt | ile kosztuje OC przyczepki |
| porównanie | OC przyczepki czy w polisie samochodu |
| wyjątek, warunek | przyczepka bez OC kara UFG |
| problem, błąd | przyczepka niezarejestrowana a OC |
| dla kogo | ubezpieczenie przyczepki kempingowej |
| lokalne, prawne | przepisy OC przyczepki 2026 |
| decyzja | czy warto AC na przyczepkę |

## Format pliku

```json
{
  "fraza": "ubezpieczenie przyczepki",
  "zapytania": [
    {"q": "czy przyczepka musi mieć oc", "typ": "definicja"},
    {"q": "ile kosztuje oc przyczepki", "typ": "koszt"}
  ]
}
```

Zapisz jako `ig-[slug]/fanout.json`. Typ służy potem do wykrycia luk: zapytanie, na które żadna pobrana strona nie odpowiada, to kandydat na sekcję artykułu.
