# 🧪 Odcinek 1 — skrypty i zmierzone dane

[![Ollama](https://img.shields.io/badge/Ollama-0.40.11-blue)]()
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)]()
[![Powtórzone](https://img.shields.io/badge/Powt%C3%B3rzone_26.10.2026-identycznie_przy_T%3D0-success)]()

> 🎯 Skrypty, z których powstała każda liczba w odcinku 1, i zmierzone wyniki użyte w filmie. Przewodnik, który je
> objaśnia — z tymi samymi zapytaniami jako pojedyncze komendy do wpisania samemu: [docs/01-llm-and-tokens_PL.md](../../docs/01-llm-and-tokens_PL.md)
> · [EN](../../docs/01-llm-and-tokens.md). 🇬🇧 [English version of this file](README.md)

To **ścieżka skryptowa**: wszystkie pomiary z filmu jednym poleceniem. Jeśli zaczynasz — idź do przewodnika,
sekcja „Zrób sam”; tu wrócisz, gdy zechcesz sprawdzić wszystkie liczby naraz.

## 📦 Co tu jest

| Plik | Co robi |
|---|---|
| `tokens.py` | tnie przykładowe zdania na tokeny trzema tokenizerami (GPT-4o, Llama 3.2, Gemma 3) i je liczy |
| `next_token.py` | pyta lokalne modele w Ollamie o liczbę tokenów, kandydatów na następny token (`logprobs`) i robi test temperatury |
| `make_svgs.py` | rysuje grafiki przewodnika (`docs/img/01/*.svg`) prosto z `data/` |
| `requirements.txt` | pakiety Pythona dla `tokens.py` (pozostałe dwa skrypty korzystają tylko z biblioteki standardowej) |
| `data/` | **zmierzone wyniki z 26.10.2026** — liczby pokazane w filmie |
| `results/` | tu trafiają Twoje uruchomienia (nie idą do repo), żeby `data/` zostało takie, jak zmierzone |

## 🚀 Uruchomienie

Potrzebujesz Ollamy z modelami z przewodnika (sekcja *Instalacja Ollamy i modeli*; tu potrzebne są wszystkie trzy,
także `gemma4`) i Pythona 3.10+.

**PowerShell**

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python tokens.py          # -> results\tokens.json (sekundy; raz pobiera dwa pliki tokenizerów)
.venv\Scripts\python next_token.py      # -> results\next_token.json (kilka minut, trzy modele)
```

**Bash** (Linux, macOS)

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python tokens.py
.venv/bin/python next_token.py
```

## ✅ Porównaj z naszymi

- `results/tokens.json` musi być **identyczny** z `data/tokens.json` — tokenizer to stała tabela.
- W `results/next_token.json` liczby tokenów, kandydaci i odpowiedzi przy temperaturze 0 powinny zgadzać się z `data/`;
  próby przy temperaturze 0,7 i 1,5 są losowe i **będą** inne.
- Nasze własne ponowne uruchomienie tych skryptów 26.10.2026 (ta sama Ollama 0.40.11) zgodziło się z `data/` dokładnie
  we wszystkim powyżej. Po samoczynnej aktualizacji Ollamy do 0.40.13 (30.10.2026) liczniki, kandydaci i odpowiedzi
  przy temperaturze 0 nadal się zgadzały, ale procenty Llamy 3.2 i Bielika przesunęły się o kilka punktów — tak działa
  inna wersja Ollamy albo modelu.
- `next_token.py` przed każdym pomiarem kandydatów wyładowuje model (tak jak `ollama stop`): zapamiętany początek
  zapytania zmienia końcowe cyfry prawdopodobieństw (77,7% ze świeżego modelu, 78,1% z zapamiętanego).
- Na innym sprzęcie (inna karta graficzna, sam procesor) procenty mogą się różnić o kilka punktów; liczy się odpowiedź
  i kolejność głównych kandydatów (na czystym Windows 10 bez karty graficznej: różnice 0,2–3 punktu, ta sama odpowiedź).

Pliki tokenizerów pobierają się przy pierwszym uruchomieniu z ich publicznych kopii; nie są przechowywane w tym repo.
