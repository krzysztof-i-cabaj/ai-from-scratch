# ==============================================================================
# Title:        tokens.py
# Description:  Cuts the episode-1 sentences into tokens with three tokenizers (GPT-4o, Llama 3.2, Gemma 3)
#               and counts them; this is where the "32 vs 22 blocks" in the video comes from
#
# Author:       KCB Kris
# Date:         2026-10-30
# Version:      1.1
#
# Requirements: - Python 3.10+, packages from requirements.txt (tokenizers, tiktoken, requests)
#               - internet on the first run (tokenizer.json from public copies on Hugging Face, cached next to the script)
#
# Usage:        python tokens.py            -> results/tokens.json + console preview
#               python tokens.py --out data -> overwrite the measured file (not needed to reproduce)
# ==============================================================================
"""How different models cut the same sentence into tokens."""

import argparse
import json
import sys
from pathlib import Path

import requests
import tiktoken
from tokenizers import Tokenizer

HERE = Path(__file__).resolve().parent

# Public, ungated copies of the tokenizers (the official repositories require accepting a licence first).
HF_TOKENIZERS = {
    "Llama 3.2": "unsloth/Llama-3.2-1B-Instruct",
    "Gemma 3": "unsloth/gemma-3-4b-it",
}

SENTENCES = {
    "forest_pl": "W sobotę rano pojechaliśmy z dziećmi do lasu na grzyby i wróciliśmy z pełnym koszykiem.",
    "forest_en": "On Saturday morning we went to the forest with the kids to pick mushrooms and came back with a full basket.",
    "sea_pl": "Na wakacje najchętniej jeżdżę nad morze.",
    "sea_en": "On holiday I like to go to the seaside most.",
    "pet_pl": "Najlepsze zwierzę domowe to pies.",
    "pet_en": "The best pet is a dog.",
}


def hf_tokenizer(repo: str) -> Tokenizer:
    """Download tokenizer.json once, then load it from the local copy."""
    cache = HERE / (repo.replace("/", "__") + ".tokenizer.json")
    if not cache.exists():
        resp = requests.get(f"https://huggingface.co/{repo}/resolve/main/tokenizer.json", timeout=60)
        resp.raise_for_status()
        cache.write_bytes(resp.content)
    return Tokenizer.from_file(str(cache))


def pieces_hf(tok: Tokenizer, text: str) -> list[str]:
    """Token pieces as substrings of the original text (offsets), without special tokens."""
    enc = tok.encode(text, add_special_tokens=False)
    return [text[a:b] for a, b in enc.offsets]


def pieces_tiktoken(enc, text: str) -> list[str]:
    """Token pieces for tiktoken; a token that splits a letter's bytes is merged into the next piece.
    For the sentences here the number of pieces equals the number of token ids (checked)."""
    ids = enc.encode(text)
    _, offsets = enc.decode_with_offsets(ids)
    bounds = offsets + [len(text)]
    out = [text[bounds[i]:bounds[i + 1]] for i in range(len(ids))]
    return [p for p in out if p]


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", default="results", help="output folder next to the script (default: results)")
    out_dir = HERE / ap.parse_args().out
    out_dir.mkdir(exist_ok=True)

    splitters = {"ChatGPT (GPT-4o)": lambda t, e=tiktoken.get_encoding("o200k_base"): pieces_tiktoken(e, t)}
    for name, repo in HF_TOKENIZERS.items():
        splitters[name] = lambda t, k=hf_tokenizer(repo): pieces_hf(k, t)

    result = {"sentences": SENTENCES, "tokenizers": {}}
    for name, split in splitters.items():
        result["tokenizers"][name] = {}
        print(f"\n=== {name}")
        for key, text in SENTENCES.items():
            pieces = split(text)
            result["tokenizers"][name][key] = {"count": len(pieces), "pieces": pieces}
            print(f"{key:10} {len(pieces):3}  " + "|".join(pieces))

    print("\n=== PL/EN")
    for name, rows in result["tokenizers"].items():
        ratios = [f"{k[:-3]} {rows[k]['count']}/{rows[k[:-3] + '_en']['count']} = "
                  f"{rows[k]['count'] / rows[k[:-3] + '_en']['count']:.2f}x"
                  for k in rows if k.endswith("_pl")]
        print(f"{name:18} " + " | ".join(ratios))

    (out_dir / "tokens.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n")
    print(f"\nsaved: {out_dir / 'tokens.json'}")


if __name__ == "__main__":
    main()
