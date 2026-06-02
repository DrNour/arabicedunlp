"""Arabic text normalization utilities.

The functions are intentionally transparent and rule based. They are meant for
reproducible classroom and corpus analytics rather than opaque preprocessing.
"""

from __future__ import annotations

import re

ARABIC_DIACRITICS_RE = re.compile(r"[\u064B-\u065F\u0670]")
TATWEEL = "\u0640"


def remove_diacritics(text: str | None) -> str:
    """Remove common Arabic diacritics from text.

    Parameters
    ----------
    text:
        Input text. ``None`` is treated as an empty string.
    """
    if text is None:
        return ""
    return ARABIC_DIACRITICS_RE.sub("", str(text))


def normalize_alef(text: str | None) -> str:
    """Normalize Alef variants to bare Alef."""
    if text is None:
        return ""
    return re.sub(r"[إأآٱ]", "ا", str(text))


def normalize_yaa(text: str | None) -> str:
    """Normalize Alef Maqsura to Yaa."""
    if text is None:
        return ""
    return str(text).replace("ى", "ي")


def normalize_taa_marbuta(text: str | None, target: str = "ه") -> str:
    """Normalize Taa Marbuta.

    Parameters
    ----------
    target:
        Either ``"ه"`` or ``"ة"``. The default is ``"ه"`` for conservative
        surface-form normalization in simple edit-distance workflows.
    """
    if target not in {"ه", "ة"}:
        raise ValueError("target must be either 'ه' or 'ة'")
    if text is None:
        return ""
    return str(text).replace("ة", target)


def normalize_arabic(
    text: str | None,
    *,
    remove_diacritic_marks: bool = True,
    normalize_alef_forms: bool = True,
    normalize_yaa_forms: bool = True,
    normalize_taa: bool = False,
    remove_tatweel: bool = True,
) -> str:
    """Apply a transparent Arabic normalization pipeline.

    The default keeps Taa Marbuta unchanged because this can be important for
    linguistically meaningful Arabic comparison. Use ``normalize_taa=True`` if
    a more aggressive surface normalization is required.
    """
    out = "" if text is None else str(text)
    if remove_tatweel:
        out = out.replace(TATWEEL, "")
    if remove_diacritic_marks:
        out = remove_diacritics(out)
    if normalize_alef_forms:
        out = normalize_alef(out)
    if normalize_yaa_forms:
        out = normalize_yaa(out)
    if normalize_taa:
        out = normalize_taa_marbuta(out)
    return out
