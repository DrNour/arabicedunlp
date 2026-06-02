from arabicedunlp import word_tokenize, token_edit_distance, compare_texts


def test_word_tokenize_arabic_english():
    text = "جامعة الإمارات (UAEU) ممتازة."
    assert "جامعة" in word_tokenize(text)
    assert "UAEU" in word_tokenize(text)


def test_token_edit_distance():
    assert token_edit_distance("the student writes", "the student writes") == 0
    assert token_edit_distance("the student writes", "the student revises") == 1


def test_compare_texts():
    result = compare_texts("A B C", "A B D")
    assert result.edit_distance == 1
    assert round(result.edit_ratio, 3) == 0.333
