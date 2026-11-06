# ==============================================================================
# Title:        make_svgs.py
# Description:  Draws the episode-1 diagrams (SVG, English + Polish) straight from the measured data in data/,
#               so the numbers on the pictures always match the tables in the guide
#
# Author:       KCB Kris
# Date:         2026-10-30
# Version:      1.1
#
# Requirements: - Python 3.10+ (standard library only)
#
# Usage:        python make_svgs.py   -> ../../docs/img/01/{tokens-three-tokenizers,bees-step-by-step,temperature}[_pl].svg
# ==============================================================================
"""Episode 1 diagrams from data/tokens.json and data/next_token.json."""

import json
import math
from pathlib import Path
from xml.sax.saxutils import escape

HERE = Path(__file__).resolve().parent
OUT = HERE.parents[1] / "docs" / "img" / "01"
TOK = json.loads((HERE / "data" / "tokens.json").read_text(encoding="utf-8"))
NXT = json.loads((HERE / "data" / "next_token.json").read_text(encoding="utf-8"))

# colours of the video (navy theme)
BG, PANEL, LINE, FG, MUTED = "#0e1f33", "#18304a", "#2c4763", "#eef3f8", "#9fb3c8"
ACCENT, BLUE, GREEN, RED, VIOLET = "#f2a65a", "#5bc8f5", "#7fd68b", "#ef7b6c", "#b59cf5"
PALETTE = [ACCENT, BLUE, GREEN, RED, VIOLET]
SANS = "Segoe UI, Helvetica, Arial, sans-serif"
MONO = "Consolas, 'DejaVu Sans Mono', Menlo, monospace"
MONO_W = 0.6                                         # monospace character width in em (safe upper bound)

T = {  # texts: (English, Polish)
    "tok_title": ("The same sentence, three tokenizers", "To samo zdanie, trzy tokenizery"),
    "en_row": ("ChatGPT (GPT-4o) · the same sentence in English", "ChatGPT (GPT-4o) · to samo zdanie po angielsku"),
    "tok_src": ("tiktoken o200k_base · tokenizer.json of Llama 3.2 and Gemma 3 · counted 26 Oct 2026",
                "tiktoken o200k_base · tokenizer.json Llama 3.2 i Gemma 3 · policzone 26.10.2026"),
    "bees_title": ("Where the bees came from: one block at a time", "Skąd pszczoły: klocek po klocku"),
    "step": ("step", "krok"),
    "so_far": ("so far", "mamy"),
    "picked": ("picked", "wybór"),
    "bees_note": ("“psy” (dogs) was second in step 1 — but the model never goes back.",
                  "„psy” było drugie w kroku 1 — ale model nigdy się nie cofa."),
    "bees_src": ("Llama 3.2 (3B) · Ollama 0.40.11 · temperature 0 · logprobs, top 5 · measured 26 Oct 2026",
                 "Llama 3.2 (3B) · Ollama 0.40.11 · temperatura 0 · logprobs, top 5 · pomiar 26.10.2026"),
    "temp_title": ("Temperature: how much the model gambles", "Temperatura: jak bardzo model losuje"),
    "chances": ("chances of the first block, recomputed as p^(1/T)", "szanse pierwszego klocka, przeliczone p^(1/T)"),
    "runs": ("the same question 5 times — first word of the answer", "to samo pytanie 5 razy — pierwsze słowo odpowiedzi"),
    "temp_src": ("Bielik 11B v3 · Ollama 0.40.11 · measured 26 Oct 2026 · at T > 0 your runs will differ",
                 "Bielik 11B v3 · Ollama 0.40.11 · pomiar 26.10.2026 · przy T > 0 Twoje wyniki będą inne"),
}


def tr(key: str, pl: bool) -> str:
    return T[key][1 if pl else 0]


def blocks_label(n: int, pl: bool) -> str:
    """"32 blocks" / Polish plural: 1 klocek, 2-4 klocki (not 12-14), otherwise klocków."""
    if not pl:
        return f"{n} block" if n == 1 else f"{n} blocks"
    if n == 1:
        return "1 klocek"
    if n % 10 in (2, 3, 4) and n % 100 not in (12, 13, 14):
        return f"{n} klocki"
    return f"{n} klocków"


def num(x: float, pl: bool) -> str:
    s = f"{x:.1f}"
    return s.replace(".", ",") if pl else s


def text(x, y, s, size=16, fill=FG, anchor="start", weight=None, font=SANS, extra=""):
    w = f' font-weight="{weight}"' if weight else ""
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{font}" font-size="{size}" fill="{fill}" '
            f'text-anchor="{anchor}"{w}{extra}>{escape(s)}</text>')


def svg(width, height, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">\n'
            f'  <title>{escape(title)}</title>\n  <rect width="{width}" height="{height}" rx="18" fill="{BG}"/>\n  '
            + "\n  ".join(body) + "\n</svg>\n")


def block_row(pieces, x0, y, max_x, size=19):
    """Token pieces as coloured blocks; a leading space becomes a wider gap. Returns (svg parts, bottom y)."""
    parts, x, h = [], x0, size * 1.6
    for i, p in enumerate(pieces):
        word = p.lstrip(" ")
        gap = 12 if (p != word and i) else 3
        w = len(word) * size * MONO_W + 14
        if x + gap + w > max_x:
            x, y = x0, y + h + 10
        else:
            x += gap if i else 0
        c = PALETTE[i % len(PALETTE)]
        parts.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="6" fill="{c}" '
                     f'fill-opacity="0.18" stroke="{c}" stroke-width="2"/>')
        parts.append(text(x + w / 2, y + h * 0.7, word, size, FG, "middle", font=MONO))
        x += w
    return parts, y + h


def tokens_svg(pl: bool) -> str:
    W = 1100
    body = [text(40, 52, tr("tok_title", pl), 26, FG, weight=700)]
    sent = TOK["sentences"]["forest_pl"]
    body.append(text(40, 84, f"„{sent}”" if pl else f"“{sent}”", 15, MUTED, extra=' font-style="italic"'))
    y = 120
    rows = [(name, data["forest_pl"]["pieces"]) for name, data in TOK["tokenizers"].items()]
    rows.append((tr("en_row", pl), TOK["tokenizers"]["ChatGPT (GPT-4o)"]["forest_en"]["pieces"]))
    for k, (name, pieces) in enumerate(rows):
        if k == len(rows) - 1:
            body.append(f'<line x1="40" y1="{y - 8}" x2="{W - 40}" y2="{y - 8}" stroke="{LINE}" stroke-width="2"/>')
            y += 14
        body.append(text(40, y + 16, name, 15, BLUE, weight=700, extra=' letter-spacing="0.5"'))
        body.append(text(W - 40, y + 16, blocks_label(len(pieces), pl), 18, ACCENT, "end", 700))
        parts, bottom = block_row(pieces, 40, y + 28, W - 40)
        body += parts
        y = bottom + 34
    body.append(text(40, y, tr("tok_src", pl), 13, MUTED, font=MONO))
    return svg(W, int(y + 26), body, tr("tok_title", pl))


def bees_svg(pl: bool) -> str:
    steps = NXT["candidates"]["Llama 3.2"]["pet"]["steps"]
    W, colw, x0, top = 1100, 250, 40, 80
    body = [text(40, 52, tr("bees_title", pl), 26, FG, weight=700)]
    so_far = "…to"
    for i, cands in enumerate(steps):
        x = x0 + i * (colw + 13)
        pick = cands[0]["token"]
        body.append(f'<rect x="{x}" y="{top}" width="{colw}" height="300" rx="12" fill="{PANEL}"/>')
        body.append(text(x + 16, top + 30, f"{tr('step', pl).upper()} {i + 1}", 14, BLUE, weight=700,
                         extra=' letter-spacing="1.5"'))
        body.append(text(x + 16, top + 56, f"{tr('so_far', pl)}: {so_far}", 15, MUTED))
        for j, c in enumerate(cands):
            y = top + 80 + j * 40
            bar = (colw - 136) * c["p"] / 100
            body.append(text(x + 16, y + 17, c["token"], 18, FG, weight=700 if j == 0 else None, font=MONO))
            body.append(f'<rect x="{x + 62}" y="{y + 3}" width="{colw - 136}" height="18" rx="4" fill="{BG}"/>')
            body.append(f'<rect x="{x + 62}" y="{y + 3}" width="{max(bar, 2):.1f}" height="18" rx="4" '
                        f'fill="{ACCENT if j == 0 else BLUE}"/>')
            body.append(text(x + colw - 12, y + 17, f"{num(c['p'], pl)}%", 14, FG, "end", font=MONO))
        body.append(text(x + 16, top + 286, f"{tr('picked', pl)}: {pick}", 16, ACCENT, weight=700))
        if i < len(steps) - 1:
            ax = x + colw + 1
            body.append(f'<path d="M{ax} {top + 150} l11 0 l-5 -6 m5 6 l-5 6" stroke="{ACCENT}" stroke-width="2" fill="none"/>')
        so_far = "ps" if i == 0 else so_far.replace("…to", "") + pick
    word = "".join(s[0]["token"] for s in steps)
    body.append(text(40, top + 350, f"= {word}", 34, ACCENT, weight=700, font="Georgia, serif",
                     extra=' font-style="italic"'))
    body.append(text(300, top + 343, tr("bees_note", pl), 17, FG))
    body.append(text(40, top + 386, tr("bees_src", pl), 13, MUTED, font=MONO))
    return svg(W, top + 410, body, tr("bees_title", pl))


def first_word(s: str) -> str:
    return s.replace("\r", "").strip().split("\n")[0].split(".")[0].strip().strip("*") or s.strip()


def temperature_svg(pl: bool) -> str:
    W = 1100
    first = [s for s in NXT["candidates"]["Bielik 11B v3"]["pet"]["steps"] if s[0]["token"].strip()][0][:3]
    labels = ["pies", "kot", "Pies"] if pl else ["pies (dog)", "kot (cat)", "Pies (Dog)"]
    runs = NXT["temperature"]["Bielik 11B v3"]
    body = [text(40, 52, tr("temp_title", pl), 26, FG, weight=700),
            text(40, 92, tr("chances", pl).upper(), 13, BLUE, weight=700, extra=' letter-spacing="1.2"'),
            text(570, 92, tr("runs", pl).upper(), 13, BLUE, weight=700, extra=' letter-spacing="1.2"')]
    for r, (tkey, tval) in enumerate((("0.0", 0.0), ("0.7", 0.7), ("1.5", 1.5))):
        y = 118 + r * 128
        body.append(f'<rect x="30" y="{y - 8}" width="{W - 60}" height="116" rx="12" fill="{PANEL}"/>')
        tlabel = "T = " + num(tval, pl).replace(",0", "").replace(".0", "")
        body.append(text(48, y + 22, tlabel, 20, ACCENT, weight=700, font=MONO))
        w = [c["p"] ** (1 / max(tval, 0.05)) for c in first]
        tot = sum(w)
        for j, (lab, wj) in enumerate(zip(labels, w)):
            yy = y + 38 + j * 22
            share = 100 * wj / tot
            body.append(text(48, yy + 13, lab, 14, FG, font=MONO))
            body.append(f'<rect x="170" y="{yy + 2}" width="300" height="14" rx="3" fill="{BG}"/>')
            body.append(f'<rect x="170" y="{yy + 2}" width="{max(3 * share, 2):.1f}" height="14" rx="3" '
                        f'fill="{ACCENT if j == 0 else BLUE}"/>')
            body.append(text(480, yy + 14, f"{num(share, pl)}%", 13, FG, font=MONO))
        for k, s in enumerate(runs[tkey]):
            word = first_word(s)
            odd = word.lower() != "pies"
            cx = 570 + k * 98
            c = ACCENT if odd else LINE
            body.append(f'<rect x="{cx}" y="{y + 30}" width="88" height="44" rx="8" fill="{c}" '
                        f'fill-opacity="{0.25 if odd else 0.6}" stroke="{c}" stroke-width="2"/>')
            body.append(text(cx + 44, y + 59, word, 17, FG, "middle", 700 if odd else None))
    body.append(text(40, 118 + 3 * 128 + 6, tr("temp_src", pl), 13, MUTED, font=MONO))
    return svg(W, 118 + 3 * 128 + 30, body, tr("temp_title", pl))


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for name, fn in (("tokens-three-tokenizers", tokens_svg), ("bees-step-by-step", bees_svg),
                     ("temperature", temperature_svg)):
        for pl in (False, True):
            path = OUT / f"{name}{'_pl' if pl else ''}.svg"
            path.write_text(fn(pl), encoding="utf-8", newline="\n")
            print("saved:", path.relative_to(HERE.parents[1]))


if __name__ == "__main__":
    main()
