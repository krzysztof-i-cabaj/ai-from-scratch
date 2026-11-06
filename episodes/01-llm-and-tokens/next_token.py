# ==============================================================================
# Title:        next_token.py
# Description:  Measurements in a local Ollama for episode 1: Polish/English token counts, next-token candidates
#               with their probabilities, and the same question asked several times at three temperatures
#
# Author:       KCB Kris
# Date:         2026-10-30
# Version:      1.2
#
# Requirements: - Ollama with logprobs support (checked on 0.40.11) running on localhost:11434
#               - the models from MODELS pulled (ollama pull ...)
#               - Python 3.10+ (standard library only)
#
# Usage:        python next_token.py [--runs 5] [--out results]   -> results/next_token.json + console preview
# ==============================================================================
"""Episode 1 measurements. Prompts are sent from Python on purpose: passing Polish text through shell
arguments (curl in Git Bash) corrupted the characters and changed the counts."""

import argparse
import json
import math
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
OLLAMA = "http://localhost:11434/api/generate"

MODELS = {
    "Bielik 11B v3": "SpeakLeash/bielik-11b-v3.0-instruct:Q4_K_M",
    "Gemma 4": "gemma4",
    "Llama 3.2": "llama3.2",
}

COUNT_TEXTS = {
    "forest_pl": "W sobotę rano pojechaliśmy z dziećmi do lasu na grzyby i wróciliśmy z pełnym koszykiem.",
    "forest_en": "On Saturday morning we went to the forest with the kids to pick mushrooms and came back with a full basket.",
    "dba_pl": "Administrator bazy danych sprawdza wydajność zapytań i optymalizuje indeksy.",
    "dba_en": "The database administrator checks query performance and optimizes indexes.",
}

PREFIX = "Dokończ zdanie jednym słowem: "          # "Finish the sentence with one word: "
PROMPTS = {
    "pet": "Najlepsze zwierzę domowe to",           # The best pet is
    "sea": "Na wakacje najchętniej jeżdżę nad",     # On holiday I like to go to the
    "drink": "Najlepszy napój na poranek to",       # The best morning drink is
    "database": "Najlepsza baza danych to",         # The best database is
}
TEMPERATURES = [0.0, 0.7, 1.5]


def generate(model: str, prompt: str, **extra) -> dict:
    body = {"model": model, "prompt": prompt, "stream": False, "think": False, **extra}
    req = urllib.request.Request(OLLAMA, data=json.dumps(body).encode("utf-8"),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=600) as resp:
        return json.load(resp)


def unload(model: str) -> None:
    """Same as `ollama stop <model>`: a cached prompt would change the last digits of the probabilities."""
    body = json.dumps({"model": model, "keep_alive": 0}).encode("utf-8")
    req = urllib.request.Request(OLLAMA, data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        resp.read()


def count_tokens(model: str, text: str) -> int:
    """prompt_eval_count in raw mode minus the single start-of-text token."""
    res = generate(model, text, raw=True, options={"num_predict": 1})
    return res["prompt_eval_count"] - 1


def candidates(model: str, prompt: str, steps: int = 4) -> dict:
    unload(model)
    res = generate(model, PREFIX + prompt, logprobs=True, top_logprobs=5,
                   options={"num_predict": steps, "temperature": 0})
    table = [[{"token": c["token"], "p": round(math.exp(c["logprob"]) * 100, 1)} for c in s["top_logprobs"]]
             for s in res.get("logprobs", [])]
    return {"answer": res["response"].strip(), "steps": table}


def samples(model: str, prompt: str, temperature: float, runs: int) -> list[str]:
    return [generate(model, PREFIX + prompt, options={"num_predict": 12, "temperature": temperature})["response"].strip()
            for _ in range(runs)]


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--runs", type=int, default=5, help="samples per temperature")
    ap.add_argument("--out", default="results", help="output folder next to the script (default: results)")
    args = ap.parse_args()
    out_dir = HERE / args.out
    out_dir.mkdir(exist_ok=True)
    out = {"counts": {}, "candidates": {}, "temperature": {}}

    for name, model in MODELS.items():
        print(f"\n######## {name}")
        counts = {k: count_tokens(model, t) for k, t in COUNT_TEXTS.items()}
        out["counts"][name] = counts
        print("tokens:", counts)

        out["candidates"][name] = {}
        for key, prompt in PROMPTS.items():
            c = candidates(model, prompt)
            out["candidates"][name][key] = c
            first = next((s for s in c["steps"] if s[0]["token"].strip()), c["steps"][0] if c["steps"] else [])
            print(f"  {prompt!r} -> {c['answer']!r} | " + " · ".join(f"{x['token']!r} {x['p']}%" for x in first))

        out["temperature"][name] = {}
        for t in TEMPERATURES:
            s = samples(model, PROMPTS["pet"], t, args.runs)
            out["temperature"][name][str(t)] = s
            print(f"  T={t}: " + " | ".join(x.replace("\n", " ") for x in s))

    (out_dir / "next_token.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n")
    print(f"\nsaved: {out_dir / 'next_token.json'}")


if __name__ == "__main__":
    main()
