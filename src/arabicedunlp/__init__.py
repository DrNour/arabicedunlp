"""ArabicEduNLP: Arabic translation and post-editing analytics.

ArabicEduNLP is a lightweight research package for analysing Arabic/English
translation and post-editing records. It provides Arabic text normalization,
word tokenization, edit-distance metrics, corpus loading, and reproducible
summary tables for NLP and translation-technology research.
"""

from .normalize import (
    remove_diacritics,
    normalize_alef,
    normalize_yaa,
    normalize_taa_marbuta,
    normalize_arabic,
)
from .tokenize import word_tokenize, arabic_word_tokenize
from .metrics import (
    levenshtein_distance,
    token_edit_distance,
    token_edit_ratio,
    compare_texts,
)
from .corpus import load_corpus, compute_record_metrics, summarize_corpus

__version__ = "0.1.0"

__all__ = [
    "remove_diacritics",
    "normalize_alef",
    "normalize_yaa",
    "normalize_taa_marbuta",
    "normalize_arabic",
    "word_tokenize",
    "arabic_word_tokenize",
    "levenshtein_distance",
    "token_edit_distance",
    "token_edit_ratio",
    "compare_texts",
    "load_corpus",
    "compute_record_metrics",
    "summarize_corpus",
]
