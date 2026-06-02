import pandas as pd
from arabicedunlp.corpus import compute_record_metrics, summarize_corpus


def test_compute_record_metrics():
    df = pd.DataFrame({
        "record_id": ["R1"],
        "student_id": ["S001"],
        "exercise_id": [1],
        "task_category": ["post_editing"],
        "source_text": ["النص الأصلي"],
        "mt_output": ["the original text"],
        "student_submission": ["the revised text"],
    })
    out = compute_record_metrics(df)
    assert "computed_mt_visible_submission_edit_distance" in out.columns
    assert out.loc[0, "computed_mt_visible_submission_edit_distance"] == 1
    summary = summarize_corpus(out)
    assert summary["number_of_records"] == 1
    assert summary["number_of_students"] == 1
