"""Report-generation helpers."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from .corpus import summarize_corpus


def group_descriptives(df: pd.DataFrame, group_col: str = "task_category") -> pd.DataFrame:
    """Return grouped descriptive statistics for common numeric variables."""
    numeric_cols = [
        "computed_source_word_count",
        "computed_mt_word_count",
        "computed_submission_word_count",
        "computed_mt_visible_submission_edit_distance",
        "computed_mt_visible_submission_edit_ratio",
        "time_spent_sec",
        "preferred_edit_count",
    ]
    cols = [c for c in numeric_cols if c in df.columns]
    if group_col not in df.columns or not cols:
        return pd.DataFrame()
    return df.groupby(group_col)[cols].agg(["count", "mean", "median", "std"]).round(4)


def write_json_report(df: pd.DataFrame, out_path: str | Path) -> None:
    """Write a compact JSON report."""
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    report = summarize_corpus(df)
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
