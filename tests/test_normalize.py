from arabicedunlp import remove_diacritics, normalize_arabic, normalize_alef


def test_remove_diacritics():
    assert remove_diacritics("كِتابٌ") == "كتاب"


def test_normalize_alef():
    assert normalize_alef("إلى آفاق أوسع") == "الى افاق اوسع"


def test_default_normalize_keeps_taa_marbuta():
    assert normalize_arabic("جامعة") == "جامعة"
