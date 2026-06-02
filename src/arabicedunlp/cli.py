"""Command-line interface for ArabicEduNLP."""

from __future__ import annotations

import argparse
from pathlib import Path

from .corpus import load_corpus, compute_record_metrics, summarize_corpus
from .reporting import group_descriptives, write_json_report
from .metrics import compare_texts


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="arabicedunlp", description="Arabic translation and post-editing analytics")
    subparsers = parser.add_subparsers(dest="command", required=True)

    compare = subparsers.add_parser("compare", help="Compare MT/reference text with a student/final text")
    compare.add_argument("reference")
    compare.add_argument("hypothesis")

    analyze = subparsers.add_parser("analyze", help="Analyze a CSV/JSONL corpus")
    analyze.add_argument("input", help="Path to corpus CSV or JSONL")
    analyze.add_argument("--out", default="outputs/report.json", help="Output JSON report path")
    analyze.add_argument("--descriptives", default=None, help="Optional CSV path for grouped descriptives")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "compare":
        result = compare_texts(args.reference, args.hypothesis).to_dict()
        for key, value in result.items():
            print(f"{key}: {value}")
        return 0

    if args.command == "analyze":
        df = load_corpus(args.input)
        df = compute_record_metrics(df)
        write_json_report(df, args.out)
        print(f"Wrote summary report to {args.out}")
        print(summarize_corpus(df))
        if args.descriptives:
            table = group_descriptives(df)
            out = Path(args.descriptives)
            out.parent.mkdir(parents=True, exist_ok=True)
            table.to_csv(out)
            print(f"Wrote grouped descriptives to {out}")
        return 0

    parser.error("Unknown command")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
