"""Corpus loading and summary utilities for ArabicEduNLP."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

import pandas as pd

from .metrics import compare_texts
from .tokenize import word_tokenize

REQUIRED_COLUMNS = [
    "record_id",
    "task_category",
    "source_text",
    "mt_output",
    "student_submission",
]


def load_corpus(path: str | Path) -> pd.DataFrame:
    """Load a CSV or JSONL corpus file.

    The loader keeps missing text fields as empty strings so downstream metrics
    remain deterministic.
    """
    path = Path(path)
    if path.suffix.lower() == ".csv":
        df = pd.read_csv(path)
    elif path.suffix.lower() in {".jsonl", ".ndjson"}:
        df = pd.read_json(path, lines=True)
    else:
        raise ValueError("Supported corpus formats are .csv and .jsonl")

    for col in ["source_text", "mt_output", "student_submission", "task_category"]:
        if col in df.columns:
            df[col] = df[col].fillna("").astype(str)
    return df


def validate_columns(df: pd.DataFrame, required: Iterable[str] = REQUIRED_COLUMNS) -> list[str]:
    """Return a list of missing required columns."""
    return [col for col in required if col not in df.columns]


def compute_record_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """Compute transparent word-count and edit-distance metrics for records."""
    missing = validate_columns(df)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    out = df.copy()
    out["computed_source_word_count"] = out["source_text"].apply(lambda x: len(word_tokenize(x)))
    out["computed_mt_word_count"] = out["mt_output"].apply(lambda x: len(word_tokenize(x)))
    out["computed_submission_word_count"] = out["student_submission"].apply(lambda x: len(word_tokenize(x)))

    comparisons = [compare_texts(mt, sub).to_dict() for mt, sub in zip(out["mt_output"], out["student_submission"])]
    comp = pd.DataFrame(comparisons)
    out["computed_mt_visible_submission_edit_distance"] = comp["edit_distance"].values
    out["computed_mt_visible_submission_edit_ratio"] = comp["edit_ratio"].values
    out["computed_visible_length_ratio"] = comp["length_ratio"].values
    return out


def summarize_corpus(df: pd.DataFrame) -> dict:
    """Create a compact corpus summary suitable for paper reporting."""
    total = len(df)
    student_count = df["student_id"].nunique() if "student_id" in df.columns else None
    exercise_count = df["exercise_id"].nunique() if "exercise_id" in df.columns else None
    categories = df["task_category"].value_counts(dropna=False).to_dict() if "task_category" in df.columns else {}

    summary = {
        "number_of_records": int(total),
        "number_of_students": None if student_count is None else int(student_count),
        "number_of_exercises": None if exercise_count is None else int(exercise_count),
        "task_categories": {str(k): int(v) for k, v in categories.items()},
    }

    numeric = [
        "computed_source_word_count",
        "computed_mt_word_count",
        "computed_submission_word_count",
        "computed_mt_visible_submission_edit_distance",
        "computed_mt_visible_submission_edit_ratio",
        "time_spent_sec",
        "preferred_edit_count",
    ]
    present = [col for col in numeric if col in df.columns]
    if present:
        summary["numeric_means"] = {col: float(df[col].dropna().mean()) for col in present}
        summary["numeric_medians"] = {col: float(df[col].dropna().median()) for col in present}

    return summary
