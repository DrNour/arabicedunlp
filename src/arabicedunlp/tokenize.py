"""Tokenization utilities for Arabic/English classroom corpora."""

from __future__ import annotations

import re

TOKEN_RE = re.compile(
    r"[\u0600-\u06FF]+|[A-Za-z]+(?:[-'][A-Za-z]+)?|\d+(?:[.,]\d+)?|[^\w\s]",
    flags=re.UNICODE,
)
ARABIC_TOKEN_RE = re.compile(r"[\u0600-\u06FF]+", flags=re.UNICODE)


def word_tokenize(text: str | None, *, lowercase_latin: bool = False) -> list[str]:
    """Tokenize Arabic/English text into words, numbers, and punctuation.

    This simple tokenizer is designed for transparent edit-distance and
    corpus-statistics workflows. It is not a replacement for a morphological
    tokenizer such as those in CAMeL Tools.
    """
    if text is None:
        return []
    tokens = TOKEN_RE.findall(str(text))
    if lowercase_latin:
        tokens = [t.lower() if re.search(r"[A-Za-z]", t) else t for t in tokens]
    return tokens


def arabic_word_tokenize(text: str | None) -> list[str]:
    """Return Arabic-script word tokens only."""
    if text is None:
        return []
    return ARABIC_TOKEN_RE.findall(str(text))
