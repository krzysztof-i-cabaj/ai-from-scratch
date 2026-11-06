# 📖 Słowniczek — AI od zera

[![Odcinki](https://img.shields.io/badge/Pojęcia_z_odcinków-1-blue)]()
[![Stan](https://img.shields.io/badge/Stan-rośnie_z_każdym_odcinkiem-success)]()
[![Język](https://img.shields.io/badge/Język-prosty-success)]()

> 🎯 Każde nowe słowo z serii w jednym, dwóch zdaniach — bez żargonu. Lista rośnie z każdym odcinkiem.
> 🇬🇧 [English version](glossary.md)

## 🧱 Odcinek 1

| Słowo | Co to znaczy |
|---|---|
| **LLM** (duży model języka) | Program, który na podstawie ogromnej ilości tekstu nauczył się zgadywać, jaki kawałek tekstu będzie następny. Na nim działają czaty AI. |
| **Token** (klocek) | Kawałek tekstu, na którym pracuje model: całe słowo, jego część albo znak. „pies” to 1 token, „jeżdżę” to kilka. |
| **Tokenizer** | Część, która tnie tekst na tokeny. Każdy model ma swój, więc to samo zdanie może mieć różną liczbę tokenów. |
| **Prawdopodobieństwo** | Szansa w procentach, że dany token będzie następny. Model liczy ją naraz dla każdego tokenu ze swojego słownika, a my oglądamy kilka najlepszych. |
| **Waga** („pokrętło”) | Jedna z miliardów liczb w modelu. Razem zapisują, co zwykle idzie po czym. |
| **Trening** | Etap przed udostępnieniem modelu, w którym ustawia się wagi na podstawie tekstu. W czasie rozmowy wagi się nie zmieniają. |
| **Halucynacja** (zmyślenie) | Odpowiedź, która brzmi pewnie, ale jest nieprawdziwa. Bierze się z tego, że model wybiera to, co pasuje, a nie sprawdza faktów. |
| **Temperatura** | Ustawienie, jak bardzo model losuje: 0 = zawsze najbardziej prawdopodobny token, wyżej = więcej losowania. |
| **Ollama** | Darmowy program do uruchamiania modeli językowych na własnym komputerze, bez wysyłania danych do internetu. |
