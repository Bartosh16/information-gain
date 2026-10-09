# -*- coding: utf-8 -*-
"""
27 źródeł information gain i matryca decyzyjna – jedno źródło prawdy dla skilla.

Uruchomione bez argumentów drukuje references/elementy-27.md:
    python scripts/elementy.py > references/elementy-27.md

Pola elementu:
    grupa     – jedna z 10 grup (9 punktów + bonus graficzny)
    nazwa     – nazwa elementu
    pelne     – kiedy tekst dostaje 2 pkt (0 = brak, 1 = ślad albo z drugiej ręki)
    koszt     – 1 = godziny, 2 = dzień do kilku dni, 3 = tygodnie
    zasob     – czego autor potrzebuje, żeby to zrobić tanio (None = niczego)
    ai        – "zrobi" | "pomoze" | "tylko_ty"
    przyklad  – jak to wygląda w tekście
"""

GRUPY = {
    "1": ("Dane własne", "wysoka"),
    "2": ("Dane zastane", "niska"),
    "B": ("Grafika i dowód użycia", "niska"),
    "3": ("Badania i testy", "wysoka"),
    "4": ("Case studies", "wysoka"),
    "5": ("Tacit knowledge", "wysoka"),
    "6": ("Wywiady i instytucje", "wysoka"),
    "7": ("Antologie", "średnia"),
    "8": ("Narzędzia i materiały do pobrania", "średnia"),
    "9": ("Wystąpienia i nagrania", "wysoka"),
}

TYPY = {
    "evergreen": "Poradnik evergreen",
    "biezacy": "Temat bieżący",
    "ymyl": "YMYL (zdrowie, pieniądze, prawo, bezpieczeństwo)",
    "oferta": "Oferta, produkt, usługa",
    "definicja": "Definicja, słownik",
    "skala": "Treść na skalę (programmatic)",
}

# ● = pasuje i się opłaca, ◐ = zależy, ○ = nie pasuje albo nie zwraca kosztu
MATRYCA = {
    #       evergreen biezacy ymyl oferta definicja skala
    "1": ("●", "◐", "●", "●", "◐", "●"),
    "2": ("●", "●", "●", "◐", "◐", "●"),
    "B": ("●", "◐", "◐", "●", "◐", "◐"),
    "3": ("●", "○", "◐", "◐", "○", "○"),
    "4": ("●", "◐", "◐", "●", "◐", "○"),
    "5": ("●", "●", "●", "●", "●", "○"),
    "6": ("●", "○", "●", "○", "○", "○"),
    "7": ("◐", "●", "◐", "○", "○", "○"),
    "8": ("●", "○", "◐", "●", "○", "●"),
    "9": ("◐", "◐", "◐", "◐", "○", "○"),
}

UZASADNIENIA = [
    "Dane własne na skalę ●: strony programmatic zasilane własną bazą to jedyna skala, której konkurencja nie skopiuje. Definicja ◐: jedna liczba z własnych danych podnosi definicję, ale raportu pod hasło słownikowe nie buduj.",
    "Dane zastane mają niską fosę: każdy sięgnie do tego samego GUS-u. Przewagę daje zestawienie kilku źródeł, nie pojedyncza liczba.",
    "Badania w temacie bieżącym ○: zanim skończysz badanie, temat ostygnie. W YMYL ◐: badanie na małej próbie w temacie zdrowia czy pieniędzy szkodzi bardziej niż jego brak.",
    "Case studies w YMYL ◐: anegdota to nie dowód, a do tego dochodzą dane osobowe i zgoda klienta.",
    "Tacit knowledge na skalę ○: AI go nie wygeneruje, więc przy każdym tekście potrzebny jest ekspert. W YMYL ●, ale każda teza ze źródłem – sprostowanie bez źródła to ryzyko, nie przewaga.",
    "Wywiady i instytucje w temacie bieżącym ○: czekanie trwa od kilku dni do kilku tygodni. Do evergreenów pasują idealnie.",
    "Antologie w evergreenie ◐: „branża w tym roku” starzeje się z kalendarzem. W temacie bieżącym ●: podsumowania roku i prognozy.",
    "Kalkulatory w YMYL ◐: błąd w kalkulatorze składki to realna szkoda czytelnika, więc testy są obowiązkowe. Na skalę ●: jeden kalkulator obsłuży wiele stron. Fosa średnia, bo vibe coding działa też dla konkurencji.",
    "Wystąpienia ◐ prawie wszędzie: pracują na autora i markę, nie na konkretną frazę.",
]

ZASOBY = {
    "dane": "własne dane: konta, sprzedaż, analityka, pomiary",
    "klienci": "dostęp do pytań klientów: obsługa, czat, reklamacje, wyszukiwarka na stronie",
    "praktyka": "autor sam robi to, o czym pisze",
    "ekspert": "dostęp do eksperta, który da się zacytować z nazwiskiem",
    "czas": "tydzień albo więcej na jeden tekst",
    "nagrania": "nagrania lub wystąpienia autora",
}

E = {
    # 1 Dane własne
    "dane_wlasne": ("1", "Dane własne, pomiary", "liczby z własnego pomiaru, kont, sprzedaży albo testu, opisane", 1, "dane", "pomoze",
                    "„W naszym sklepie 34% zwrotów to zły rozmiar” z okresem i liczbą zamówień"),
    "pytania_klientow": ("1", "Pytania klientów", "wykorzystane realne pytania z obsługi, czatu, reklamacji lub wyszukiwarki na stronie", 1, "klienci", "pomoze",
                         "sekcja „O to pytacie najczęściej” z pytaniami z prawdziwej skrzynki"),
    # 2 Dane zastane
    "dane_zastane": ("2", "Statystyki ze źródłem", "statystyki z cudzych raportów z podanym źródłem przy liczbie", 1, None, "zrobi",
                     "liczba z raportu z linkiem i rokiem obok, nie „według badań”"),
    "zestawienie": ("2", "Zestawienie rozproszonych danych", "dane z kilku źródeł zebrane w jedną tabelę, której nie ma w żadnym źródle osobno", 1, None, "zrobi",
                    "tabela cen, limitów albo parametrów z pięciu stron producentów"),
    "otwarte_dane": ("2", "Otwarte dane i rejestry", "własne wyciągnięcie danych z rejestru, GUS, dane.gov.pl, KRS, sprawozdań", 2, None, "zrobi",
                     "ranking firm z branży policzony ze sprawozdań finansowych"),
    "dokumenty": ("2", "Dokument źródłowy czytany wprost", "ustawa, OWU, regulamin, patent, dokumentacja zacytowane z oryginału, z numerem lub linkiem", 1, None, "zrobi",
                  "„§ 7 ust. 2 OWU mówi wprost…” zamiast streszczenia ze streszczenia"),
    "zmiany": ("2", "Zmiany w czasie", "jak było, co się zmieniło i kiedy – z datami", 1, None, "zrobi",
               "oś czasu zmian przepisu albo cennika, z Wayback Machine jako źródłem"),
    # Bonus
    "grafika": ("B", "Infografika, schemat, wykres", "własna grafika z treścią merytoryczną, nie stock i nie miniatura", 1, None, "zrobi",
                "schemat procesu albo wykres z danych z tekstu"),
    "dowod_uzycia": ("B", "Dowód użycia", "własne zdjęcia, zrzuty lub nagrania z faktycznego użycia opisywanej rzeczy", 1, "praktyka", "tylko_ty",
                     "zrzut z panelu, zdjęcie produktu na biurku autora"),
    # 3 Badania i testy
    "badanie": ("3", "Badanie własne", "własne badanie z metodą i próbą", 3, "czas", "pomoze",
                "analiza 500 stron z opisaną metodą i ograniczeniami"),
    "ankieta": ("3", "Ankieta", "własna ankieta z liczbą odpowiedzi", 3, "klienci", "pomoze",
                "„zapytaliśmy 212 klientów” z pytaniem i rozkładem odpowiedzi"),
    "test": ("3", "Test hands-on", "autor sprawdził coś sam (zrobił, kupił, wdrożył) i opisał wynik", 2, "praktyka", "pomoze",
             "„zamówiłem w trzech sklepach i zmierzyłem czas dostawy”"),
    # 4 Case studies
    "case_study": ("4", "Case study", "przypadek z przebiegiem i wynikiem, najlepiej własny", 2, "praktyka", "pomoze",
                   "punkt wyjścia, co zrobione, wynik w liczbach, czas"),
    "porazki": ("4", "Historia porażki", "opis, co nie zadziałało i dlaczego", 1, "praktyka", "tylko_ty",
                "„pierwsza wersja kampanii spaliła budżet, bo…”"),
    "przed_po": ("4", "Przykład przed/po", "ta sama rzecz w wersji słabej i dobrej, pokazana w tekście", 1, None, "zrobi",
                 "opis produktu bez parametrów i z dziewięcioma parametrami obok siebie"),
    # 5 Tacit knowledge
    "doswiadczenie": ("5", "Doświadczenie autora", "obserwacje i praktyka autora w pierwszej osobie, nie ogólniki", 1, "praktyka", "tylko_ty",
                      "„w co trzecim audycie widzę ten sam błąd”"),
    "wyjatki": ("5", "Wyjątki i ograniczenia", "tekst sam mówi, kiedy jego rady nie działają, komu nie pasują, ile kosztują", 1, None, "pomoze",
                "akapit „Kiedy to nie zadziała”"),
    "kryteria": ("5", "Kryteria decyzji", "porównanie opcji z jasnymi kryteriami albo rekomendacja „kiedy A, kiedy B”", 1, None, "pomoze",
                 "tabela decyzyjna albo drzewko „jeśli…, to…”"),
    "framework": ("5", "Autorski framework", "własny podział, skala, macierz lub checklista, którą da się nazwać i zacytować", 2, "praktyka", "pomoze",
                  "nazwana metoda w 4 krokach z kryterium na każdy krok"),
    "polskie_realia": ("5", "Polskie realia", "kontekst spoza angielskiego korpusu: polskie prawo, ceny w złotówkach, urzędy, rynek", 1, None, "pomoze",
                       "kwoty w zł, nazwa urzędu, numer ustawy zamiast „check local regulations”"),
    "sprostowanie": ("5", "Sprostowanie mitu", "wskazuje błąd powtarzany w temacie i podaje źródło albo dane", 1, None, "pomoze",
                     "„w połowie topu przeczytasz X, a źródło pierwotne mówi Y”"),
    # 6 Wywiady i instytucje
    "ekspert": ("6", "Wypowiedź eksperta", "wywiad lub cytat osoby z nazwiskiem, zdobyty przez autora", 2, "ekspert", "pomoze",
                "trzy zdania praktyka z nazwiskiem i funkcją"),
    "instytucja": ("6", "Zapytanie do instytucji", "odpowiedź rzecznika, urzędu, firmy albo wniosek o informację publiczną", 2, None, "pomoze",
                   "„zapytaliśmy rzecznika X, odpowiedź z 12 marca:”"),
    # 7 Antologie
    "antologia": ("7", "Antologia ekspertów", "zebrane wypowiedzi kilku ekspertów na jeden temat", 3, "ekspert", "pomoze",
                  "pięciu praktyków odpowiada na to samo pytanie"),
    # 8 Narzędzia i materiały
    "narzedzie": ("8", "Kalkulator, quiz, konfigurator", "działający element interaktywny", 2, None, "zrobi",
                  "kalkulator kosztu w artykule o kosztach"),
    "do_pobrania": ("8", "Materiał do pobrania", "szablon, arkusz, prompt, skrypt lub repo do użycia", 1, None, "zrobi",
                    "arkusz z gotowymi formułami pod artykułem"),
    # 9 Wystąpienia
    "wystapienie": ("9", "Wystąpienie lub nagranie autora", "osadzone wystąpienie, wideo albo prezentacja autora", 3, "nagrania", "tylko_ty",
                    "fragment wystąpienia z konferencji osadzony przy sekcji, której dotyczy"),
}

KOSZT = {1: "godziny", 2: "dzień–kilka dni", 3: "tygodnie"}
AI = {"zrobi": "AI zrobi (Ty sprawdzasz źródła)", "pomoze": "AI pomoże (surowiec od Ciebie)", "tylko_ty": "tylko Ty (wersja z AI to fałszerstwo)"}

assert len(E) == 27, len(E)


def dopasowanie(kr, typ):
    """Symbol matrycy dla elementu i typu treści."""
    return MATRYCA[E[kr][0]][list(TYPY).index(typ)]


def render_md():
    w = ["# 27 źródeł information gain", "",
         "Plik generowany: `python scripts/elementy.py > references/elementy-27.md`. Nie edytuj ręcznie, zmieniaj `scripts/elementy.py`.", "",
         "Ocena tekstu: 0 = brak, 1 = ślad, jeden przykład albo z drugiej ręki, 2 = pełne wykonanie jak w kolumnie „2 pkt”. Punkt za to, co tekst ROBI, nie za to, co RADZI: lista „dodaj dane z KRS” bez własnego użycia KRS to 0. Bez dowodu (cytatu albo opisu miejsca w tekście) nie ma punktu.", ""]
    for g, (gn, fosa) in GRUPY.items():
        w += [f"## {'Bonus' if g == 'B' else g}. {gn} (fosa: {fosa})", "",
              "| Id | Element | 2 pkt, gdy… | Koszt | Wymaga | Kto | Przykład |", "|---|---|---|---|---|---|---|"]
        for kr, (gg, nazwa, pelne, koszt, zasob, ai, prz) in E.items():
            if gg == g:
                w.append(f"| `{kr}` | {nazwa} | {pelne} | {KOSZT[koszt]} | {zasob or '–'} | {AI[ai]} | {prz} |")
        w.append("")
    w += ["## Matryca decyzyjna", "",
          "● pasuje i się opłaca, ◐ zależy, ○ nie pasuje albo nie zwraca kosztu. Fosa to stopień trudności skopiowania przez konkurencję. Ocena ekspercka, nie pomiar.", "",
          "| Grupa | Fosa | " + " | ".join(TYPY.values()) + " |", "|---|---|" + "---|" * len(TYPY)]
    for g, (gn, fosa) in GRUPY.items():
        w.append(f"| {gn} | {fosa} | " + " | ".join(MATRYCA[g]) + " |")
    w += ["", "Dlaczego tak:", ""] + [f"- {u}" for u in UZASADNIENIA]
    w += ["", "## Zasoby autora", "", "Brak zasobu podnosi koszt elementu o jeden poziom.", ""]
    w += [f"- `{k}` – {v}," for k, v in ZASOBY.items()]
    w[-1] = w[-1].rstrip(",") + "."
    return "\n".join(w) + "\n"


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    print(render_md(), end="")
