"""Reproduce core descriptive tables for the ArabicEduNLP manuscript.

Example:
    python scripts/reproduce_paper_tables.py --input data/sample_corpus_synthetic.csv --outdir outputs
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

# Allow running from a source checkout without installation.
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import pandas as pd

from arabicedunlp.corpus import load_corpus, compute_record_metrics, summarize_corpus
from arabicedunlp.reporting import group_descriptives


def corpus_composition(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    if "task_category" in df.columns:
        for category, group in df.groupby("task_category", dropna=False):
            rows.append({
                "task_category": category,
                "records": len(group),
                "students": group["student_id"].nunique() if "student_id" in group.columns else None,
                "exercises": group["exercise_id"].nunique() if "exercise_id" in group.columns else None,
            })
    return pd.DataFrame(rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Input CSV or JSONL corpus")
    parser.add_argument("--outdir", default="outputs", help="Directory for output tables")
    args = parser.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    df = load_corpus(args.input)
    df = compute_record_metrics(df)

    summary = summarize_corpus(df)
    (outdir / "corpus_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    corpus_composition(df).to_csv(outdir / "table_corpus_composition.csv", index=False)
    group_descriptives(df).to_csv(outdir / "table_descriptives_by_task.csv")

    numeric_cols = [
        "computed_source_word_count",
        "computed_mt_word_count",
        "computed_submission_word_count",
        "computed_mt_visible_submission_edit_distance",
        "computed_mt_visible_submission_edit_ratio",
        "time_spent_sec",
        "preferred_edit_count",
    ]
    present = [c for c in numeric_cols if c in df.columns]
    if present:
        df[present].describe().T.round(4).to_csv(outdir / "table_overall_numeric_descriptives.csv")

    print(f"Wrote tables to {outdir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
