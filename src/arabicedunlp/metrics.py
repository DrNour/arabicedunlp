"""Transparent metrics for translation and post-editing analytics."""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Sequence

from .normalize import normalize_arabic
from .tokenize import word_tokenize


def levenshtein_distance(a: Sequence[str], b: Sequence[str]) -> int:
    """Compute Levenshtein edit distance between two token sequences.

    The operation costs for insertion, deletion, and substitution are all 1.
    The implementation uses two rows of dynamic programming to avoid large
    memory use for longer texts.
    """
    if a == b:
        return 0
    if len(a) == 0:
        return len(b)
    if len(b) == 0:
        return len(a)
    if len(a) < len(b):
        a, b = b, a
    previous = list(range(len(b) + 1))
    for i, item_a in enumerate(a, start=1):
        current = [i]
        for j, item_b in enumerate(b, start=1):
            insertion = current[j - 1] + 1
            deletion = previous[j] + 1
            substitution = previous[j - 1] + (item_a != item_b)
            current.append(min(insertion, deletion, substitution))
        previous = current
    return previous[-1]


def token_edit_distance(reference: str | None, hypothesis: str | None, *, normalize: bool = True) -> int:
    """Token-level edit distance between two strings."""
    if normalize:
        reference = normalize_arabic(reference)
        hypothesis = normalize_arabic(hypothesis)
    return levenshtein_distance(word_tokenize(reference), word_tokenize(hypothesis))


def token_edit_ratio(reference: str | None, hypothesis: str | None, *, normalize: bool = True) -> float:
    """Token-level edit ratio normalized by the reference length.

    The ratio is ``distance / max(reference_token_count, 1)``. In this package,
    the MT output is usually the reference and the student/final submission is
    the hypothesis.
    """
    ref_text = normalize_arabic(reference) if normalize else ("" if reference is None else str(reference))
    hyp_text = normalize_arabic(hypothesis) if normalize else ("" if hypothesis is None else str(hypothesis))
    ref_tokens = word_tokenize(ref_text)
    hyp_tokens = word_tokenize(hyp_text)
    return levenshtein_distance(ref_tokens, hyp_tokens) / max(len(ref_tokens), 1)


@dataclass(frozen=True)
class TextComparison:
    """Comparison output for two texts."""

    reference_tokens: int
    hypothesis_tokens: int
    edit_distance: int
    edit_ratio: float
    length_ratio: float

    def to_dict(self) -> dict[str, float | int]:
        return asdict(self)


def compare_texts(reference: str | None, hypothesis: str | None, *, normalize: bool = True) -> TextComparison:
    """Compare two texts with token length, edit distance, and ratios."""
    ref_text = normalize_arabic(reference) if normalize else ("" if reference is None else str(reference))
    hyp_text = normalize_arabic(hypothesis) if normalize else ("" if hypothesis is None else str(hypothesis))
    ref_tokens = word_tokenize(ref_text)
    hyp_tokens = word_tokenize(hyp_text)
    distance = levenshtein_distance(ref_tokens, hyp_tokens)
    ref_len = max(len(ref_tokens), 1)
    return TextComparison(
        reference_tokens=len(ref_tokens),
        hypothesis_tokens=len(hyp_tokens),
        edit_distance=distance,
        edit_ratio=distance / ref_len,
        length_ratio=len(hyp_tokens) / ref_len,
    )
