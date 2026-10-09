# Instrukcja dla agenta

To repo zawiera jeden skill: `skills/ig-sugestie/`.

Gdy użytkownik pyta, co dodać do artykułu, prosi o sugestie information gain albo podaje frazę i chce wiedzieć, czym wyróżnić tekst na tle topu Google:

1. Przeczytaj `skills/ig-sugestie/SKILL.md` i wykonuj go krok po kroku.
2. Skrypty uruchamiaj z katalogu `skills/ig-sugestie/` albo podawaj pełne ścieżki do `skills/ig-sugestie/scripts/`.
3. Zależności: `pip install -r skills/ig-sugestie/requirements.txt`.
4. Klucz SERP API bierz wyłącznie ze zmiennych środowiskowych albo z `.env` w katalogu roboczym. Gdy go brakuje, powiedz użytkownikowi, którą zmienną ustawić (README, sekcja „Klucz API”).
