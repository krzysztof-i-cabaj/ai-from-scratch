# 📖 Glossary — AI from Scratch

[![Episodes](https://img.shields.io/badge/Terms_from_episodes-1-blue)]()
[![Status](https://img.shields.io/badge/Status-grows_with_each_episode-success)]()
[![Language](https://img.shields.io/badge/Language-plain-success)]()

> 🎯 Every new word from the series in one or two sentences — no jargon. The list grows with each episode.
> 🇵🇱 [Wersja polska](glossary_PL.md)

## 🧱 Episode 1

| Word | What it means |
|---|---|
| **LLM** (large language model) | A program that learned from a huge amount of text to guess which piece of text comes next. AI chats run on it. |
| **Token** (block) | A piece of text the model works with: a whole word, part of a word or a character. "dog" is 1 token; the Polish "jeżdżę" is several. |
| **Tokenizer** | The part that cuts text into tokens. Each model has its own, so the same sentence can have a different number of tokens. |
| **Probability** | The chance, in percent, that a given token comes next. The model computes it for every token in its vocabulary at once and shows us the best few. |
| **Weight** ("knob") | One of billions of numbers inside the model. Together they store what usually follows what. |
| **Training** | The stage before a model is released, when the weights are set from text. During a chat the weights do not change. |
| **Hallucination** | An answer that sounds confident but is not true. It happens because the model picks what fits, not what it has checked. |
| **Temperature** | How much the model gambles: 0 = always the most likely token, higher = more randomness. |
| **Ollama** | A free program to run language models on your own computer, without sending your data to the internet. |
