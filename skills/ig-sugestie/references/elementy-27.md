# 27 źródeł information gain

Plik generowany: `python scripts/elementy.py > references/elementy-27.md`. Nie edytuj ręcznie, zmieniaj `scripts/elementy.py`.

Ocena tekstu: 0 = brak, 1 = ślad, jeden przykład albo z drugiej ręki, 2 = pełne wykonanie jak w kolumnie „2 pkt”. Punkt za to, co tekst ROBI, nie za to, co RADZI: lista „dodaj dane z KRS” bez własnego użycia KRS to 0. Bez dowodu (cytatu albo opisu miejsca w tekście) nie ma punktu.

## 1. Dane własne (fosa: wysoka)

| Id | Element | 2 pkt, gdy… | Koszt | Wymaga | Kto | Przykład |
|---|---|---|---|---|---|---|
| `dane_wlasne` | Dane własne, pomiary | liczby z własnego pomiaru, kont, sprzedaży albo testu, opisane | godziny | dane | AI pomoże (surowiec od Ciebie) | „W naszym sklepie 34% zwrotów to zły rozmiar” z okresem i liczbą zamówień |
| `pytania_klientow` | Pytania klientów | wykorzystane realne pytania z obsługi, czatu, reklamacji lub wyszukiwarki na stronie | godziny | klienci | AI pomoże (surowiec od Ciebie) | sekcja „O to pytacie najczęściej” z pytaniami z prawdziwej skrzynki |

## 2. Dane zastane (fosa: niska)

| Id | Element | 2 pkt, gdy… | Koszt | Wymaga | Kto | Przykład |
|---|---|---|---|---|---|---|
| `dane_zastane` | Statystyki ze źródłem | statystyki z cudzych raportów z podanym źródłem przy liczbie | godziny | – | AI zrobi (Ty sprawdzasz źródła) | liczba z raportu z linkiem i rokiem obok, nie „według badań” |
| `zestawienie` | Zestawienie rozproszonych danych | dane z kilku źródeł zebrane w jedną tabelę, której nie ma w żadnym źródle osobno | godziny | – | AI zrobi (Ty sprawdzasz źródła) | tabela cen, limitów albo parametrów z pięciu stron producentów |
| `otwarte_dane` | Otwarte dane i rejestry | własne wyciągnięcie danych z rejestru, GUS, dane.gov.pl, KRS, sprawozdań | dzień–kilka dni | – | AI zrobi (Ty sprawdzasz źródła) | ranking firm z branży policzony ze sprawozdań finansowych |
| `dokumenty` | Dokument źródłowy czytany wprost | ustawa, OWU, regulamin, patent, dokumentacja zacytowane z oryginału, z numerem lub linkiem | godziny | – | AI zrobi (Ty sprawdzasz źródła) | „§ 7 ust. 2 OWU mówi wprost…” zamiast streszczenia ze streszczenia |
| `zmiany` | Zmiany w czasie | jak było, co się zmieniło i kiedy – z datami | godziny | – | AI zrobi (Ty sprawdzasz źródła) | oś czasu zmian przepisu albo cennika, z Wayback Machine jako źródłem |

## Bonus. Grafika i dowód użycia (fosa: niska)

| Id | Element | 2 pkt, gdy… | Koszt | Wymaga | Kto | Przykład |
|---|---|---|---|---|---|---|
| `grafika` | Infografika, schemat, wykres | własna grafika z treścią merytoryczną, nie stock i nie miniatura | godziny | – | AI zrobi (Ty sprawdzasz źródła) | schemat procesu albo wykres z danych z tekstu |
| `dowod_uzycia` | Dowód użycia | własne zdjęcia, zrzuty lub nagrania z faktycznego użycia opisywanej rzeczy | godziny | praktyka | tylko Ty (wersja z AI to fałszerstwo) | zrzut z panelu, zdjęcie produktu na biurku autora |

## 3. Badania i testy (fosa: wysoka)

| Id | Element | 2 pkt, gdy… | Koszt | Wymaga | Kto | Przykład |
|---|---|---|---|---|---|---|
| `badanie` | Badanie własne | własne badanie z metodą i próbą | tygodnie | czas | AI pomoże (surowiec od Ciebie) | analiza 500 stron z opisaną metodą i ograniczeniami |
| `ankieta` | Ankieta | własna ankieta z liczbą odpowiedzi | tygodnie | klienci | AI pomoże (surowiec od Ciebie) | „zapytaliśmy 212 klientów” z pytaniem i rozkładem odpowiedzi |
| `test` | Test hands-on | autor sprawdził coś sam (zrobił, kupił, wdrożył) i opisał wynik | dzień–kilka dni | praktyka | AI pomoże (surowiec od Ciebie) | „zamówiłem w trzech sklepach i zmierzyłem czas dostawy” |

## 4. Case studies (fosa: wysoka)

| Id | Element | 2 pkt, gdy… | Koszt | Wymaga | Kto | Przykład |
|---|---|---|---|---|---|---|
| `case_study` | Case study | przypadek z przebiegiem i wynikiem, najlepiej własny | dzień–kilka dni | praktyka | AI pomoże (surowiec od Ciebie) | punkt wyjścia, co zrobione, wynik w liczbach, czas |
| `porazki` | Historia porażki | opis, co nie zadziałało i dlaczego | godziny | praktyka | tylko Ty (wersja z AI to fałszerstwo) | „pierwsza wersja kampanii spaliła budżet, bo…” |
| `przed_po` | Przykład przed/po | ta sama rzecz w wersji słabej i dobrej, pokazana w tekście | godziny | – | AI zrobi (Ty sprawdzasz źródła) | opis produktu bez parametrów i z dziewięcioma parametrami obok siebie |

## 5. Tacit knowledge (fosa: wysoka)

| Id | Element | 2 pkt, gdy… | Koszt | Wymaga | Kto | Przykład |
|---|---|---|---|---|---|---|
| `doswiadczenie` | Doświadczenie autora | obserwacje i praktyka autora w pierwszej osobie, nie ogólniki | godziny | praktyka | tylko Ty (wersja z AI to fałszerstwo) | „w co trzecim audycie widzę ten sam błąd” |
| `wyjatki` | Wyjątki i ograniczenia | tekst sam mówi, kiedy jego rady nie działają, komu nie pasują, ile kosztują | godziny | – | AI pomoże (surowiec od Ciebie) | akapit „Kiedy to nie zadziała” |
| `kryteria` | Kryteria decyzji | porównanie opcji z jasnymi kryteriami albo rekomendacja „kiedy A, kiedy B” | godziny | – | AI pomoże (surowiec od Ciebie) | tabela decyzyjna albo drzewko „jeśli…, to…” |
| `framework` | Autorski framework | własny podział, skala, macierz lub checklista, którą da się nazwać i zacytować | dzień–kilka dni | praktyka | AI pomoże (surowiec od Ciebie) | nazwana metoda w 4 krokach z kryterium na każdy krok |
| `polskie_realia` | Polskie realia | kontekst spoza angielskiego korpusu: polskie prawo, ceny w złotówkach, urzędy, rynek | godziny | – | AI pomoże (surowiec od Ciebie) | kwoty w zł, nazwa urzędu, numer ustawy zamiast „check local regulations” |
| `sprostowanie` | Sprostowanie mitu | wskazuje błąd powtarzany w temacie i podaje źródło albo dane | godziny | – | AI pomoże (surowiec od Ciebie) | „w połowie topu przeczytasz X, a źródło pierwotne mówi Y” |

## 6. Wywiady i instytucje (fosa: wysoka)

| Id | Element | 2 pkt, gdy… | Koszt | Wymaga | Kto | Przykład |
|---|---|---|---|---|---|---|
| `ekspert` | Wypowiedź eksperta | wywiad lub cytat osoby z nazwiskiem, zdobyty przez autora | dzień–kilka dni | ekspert | AI pomoże (surowiec od Ciebie) | trzy zdania praktyka z nazwiskiem i funkcją |
| `instytucja` | Zapytanie do instytucji | odpowiedź rzecznika, urzędu, firmy albo wniosek o informację publiczną | dzień–kilka dni | – | AI pomoże (surowiec od Ciebie) | „zapytaliśmy rzecznika X, odpowiedź z 12 marca:” |

## 7. Antologie (fosa: średnia)

| Id | Element | 2 pkt, gdy… | Koszt | Wymaga | Kto | Przykład |
|---|---|---|---|---|---|---|
| `antologia` | Antologia ekspertów | zebrane wypowiedzi kilku ekspertów na jeden temat | tygodnie | ekspert | AI pomoże (surowiec od Ciebie) | pięciu praktyków odpowiada na to samo pytanie |

## 8. Narzędzia i materiały do pobrania (fosa: średnia)

| Id | Element | 2 pkt, gdy… | Koszt | Wymaga | Kto | Przykład |
|---|---|---|---|---|---|---|
| `narzedzie` | Kalkulator, quiz, konfigurator | działający element interaktywny | dzień–kilka dni | – | AI zrobi (Ty sprawdzasz źródła) | kalkulator kosztu w artykule o kosztach |
| `do_pobrania` | Materiał do pobrania | szablon, arkusz, prompt, skrypt lub repo do użycia | godziny | – | AI zrobi (Ty sprawdzasz źródła) | arkusz z gotowymi formułami pod artykułem |

## 9. Wystąpienia i nagrania (fosa: wysoka)

| Id | Element | 2 pkt, gdy… | Koszt | Wymaga | Kto | Przykład |
|---|---|---|---|---|---|---|
| `wystapienie` | Wystąpienie lub nagranie autora | osadzone wystąpienie, wideo albo prezentacja autora | tygodnie | nagrania | tylko Ty (wersja z AI to fałszerstwo) | fragment wystąpienia z konferencji osadzony przy sekcji, której dotyczy |

## Matryca decyzyjna

● pasuje i się opłaca, ◐ zależy, ○ nie pasuje albo nie zwraca kosztu. Fosa to stopień trudności skopiowania przez konkurencję. Ocena ekspercka, nie pomiar.

| Grupa | Fosa | Poradnik evergreen | Temat bieżący | YMYL (zdrowie, pieniądze, prawo, bezpieczeństwo) | Oferta, produkt, usługa | Definicja, słownik | Treść na skalę (programmatic) |
|---|---|---|---|---|---|---|---|
| Dane własne | wysoka | ● | ◐ | ● | ● | ◐ | ● |
| Dane zastane | niska | ● | ● | ● | ◐ | ◐ | ● |
| Grafika i dowód użycia | niska | ● | ◐ | ◐ | ● | ◐ | ◐ |
| Badania i testy | wysoka | ● | ○ | ◐ | ◐ | ○ | ○ |
| Case studies | wysoka | ● | ◐ | ◐ | ● | ◐ | ○ |
| Tacit knowledge | wysoka | ● | ● | ● | ● | ● | ○ |
| Wywiady i instytucje | wysoka | ● | ○ | ● | ○ | ○ | ○ |
| Antologie | średnia | ◐ | ● | ◐ | ○ | ○ | ○ |
| Narzędzia i materiały do pobrania | średnia | ● | ○ | ◐ | ● | ○ | ● |
| Wystąpienia i nagrania | wysoka | ◐ | ◐ | ◐ | ◐ | ○ | ○ |

Dlaczego tak:

- Dane własne na skalę ●: strony programmatic zasilane własną bazą to jedyna skala, której konkurencja nie skopiuje. Definicja ◐: jedna liczba z własnych danych podnosi definicję, ale raportu pod hasło słownikowe nie buduj.
- Dane zastane mają niską fosę: każdy sięgnie do tego samego GUS-u. Przewagę daje zestawienie kilku źródeł, nie pojedyncza liczba.
- Badania w temacie bieżącym ○: zanim skończysz badanie, temat ostygnie. W YMYL ◐: badanie na małej próbie w temacie zdrowia czy pieniędzy szkodzi bardziej niż jego brak.
- Case studies w YMYL ◐: anegdota to nie dowód, a do tego dochodzą dane osobowe i zgoda klienta.
- Tacit knowledge na skalę ○: AI go nie wygeneruje, więc przy każdym tekście potrzebny jest ekspert. W YMYL ●, ale każda teza ze źródłem – sprostowanie bez źródła to ryzyko, nie przewaga.
- Wywiady i instytucje w temacie bieżącym ○: czekanie trwa od kilku dni do kilku tygodni. Do evergreenów pasują idealnie.
- Antologie w evergreenie ◐: „branża w tym roku” starzeje się z kalendarzem. W temacie bieżącym ●: podsumowania roku i prognozy.
- Kalkulatory w YMYL ◐: błąd w kalkulatorze składki to realna szkoda czytelnika, więc testy są obowiązkowe. Na skalę ●: jeden kalkulator obsłuży wiele stron. Fosa średnia, bo vibe coding działa też dla konkurencji.
- Wystąpienia ◐ prawie wszędzie: pracują na autora i markę, nie na konkretną frazę.

## Zasoby autora

Brak zasobu podnosi koszt elementu o jeden poziom.

- `dane` – własne dane: konta, sprzedaż, analityka, pomiary,
- `klienci` – dostęp do pytań klientów: obsługa, czat, reklamacje, wyszukiwarka na stronie,
- `praktyka` – autor sam robi to, o czym pisze,
- `ekspert` – dostęp do eksperta, który da się zacytować z nazwiskiem,
- `czas` – tydzień albo więcej na jeden tekst,
- `nagrania` – nagrania lub wystąpienia autora.
