# 🧪 Episode 1 — scripts and measured data

[![Ollama](https://img.shields.io/badge/Ollama-0.40.11-blue)]()
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)]()
[![Reproduced](https://img.shields.io/badge/Re--run_26_Oct_2026-identical_at_T%3D0-success)]()

> 🎯 The scripts that produced every number in episode 1, and the measured results used in the video. The guide that
> explains them, with the same requests as single commands to type yourself: [docs/01-llm-and-tokens.md](../../docs/01-llm-and-tokens.md)
> · [PL](../../docs/01-llm-and-tokens_PL.md). 🇵🇱 [Wersja polska tego pliku](README_PL.md)

## 📦 What's here

| File | What it does |
|---|---|
| `tokens.py` | cuts the example sentences into tokens with three tokenizers (GPT-4o, Llama 3.2, Gemma 3) and counts them |
| `next_token.py` | asks local models in Ollama for token counts, next-token candidates (`logprobs`) and runs the temperature test |
| `make_svgs.py` | draws the guide's diagrams (`docs/img/01/*.svg`) straight from `data/` |
| `requirements.txt` | Python packages for `tokens.py` (the other two use the standard library only) |
| `data/` | **the measured results from 26 Oct 2026** — the numbers shown in the video |
| `results/` | your own runs go here (not committed), so `data/` stays as it was measured |

## 🚀 Run

You need Ollama with the models from the guide (section *Installing Ollama and the models*; all three are needed
here, including `gemma4`) and Python 3.10+.

**PowerShell**

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python tokens.py          # -> results\tokens.json (seconds; downloads two tokenizer files once)
.venv\Scripts\python next_token.py      # -> results\next_token.json (a few minutes, three models)
```

**Bash** (Linux, macOS)

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python tokens.py
.venv/bin/python next_token.py
```

## ✅ Compare with ours

- `results/tokens.json` must be **identical** to `data/tokens.json` — a tokenizer is a fixed table.
- In `results/next_token.json` the counts, the candidates and the temperature-0 answers should match `data/`;
  the runs at temperature 0.7 and 1.5 are random and **will** differ.
- Our own re-run of these scripts on 26 Oct 2026 (same Ollama 0.40.11) matched `data/` exactly on all of the above.
  After Ollama updated itself to 0.40.13 (30 Oct 2026) the counts, candidates and temperature-0 answers still matched,
  but the percentages of Llama 3.2 and Bielik moved by a few points — another Ollama or model version does that.
- `next_token.py` unloads the model before each candidate measurement (same as `ollama stop`): a cached prompt changes
  the last digits of the probabilities (77.7% from a fresh model, 78.1% from a cached one).
- On different hardware (another GPU, CPU only) the percentages may differ by a few points; what matters is the answer
  and the order of the main candidates (on a clean Windows 10 with no graphics card: 0.2–3 points off, same answer).

Tokenizer files are downloaded on the first run from their public copies; they are not stored in this repository.
