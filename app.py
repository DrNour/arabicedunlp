"""Streamlit interface for ArabicEduNLP."""

from __future__ import annotations

import json
from io import BytesIO
from pathlib import Path
import tempfile

import pandas as pd
import streamlit as st

from arabicedunlp import compare_texts
from arabicedunlp.corpus import compute_record_metrics, load_corpus, summarize_corpus
from arabicedunlp.reporting import group_descriptives

st.set_page_config(page_title="ArabicEduNLP", page_icon="📝", layout="wide")

st.title("ArabicEduNLP")
st.caption("Transparent Arabic-English translation and post-editing analytics for research and teaching.")
st.info("This app supports reproducible analysis. Automatic metrics are indicators and should be interpreted with expert linguistic judgement.")

compare_tab, corpus_tab = st.tabs(["Compare two texts", "Analyse a corpus"])

with compare_tab:
    left, right = st.columns(2)
    with left:
        reference = st.text_area(
            "Reference or MT output",
            value="The university develops its academic programmes.",
            height=180,
        )
    with right:
        hypothesis = st.text_area(
            "Student submission or post-edited text",
            value="The university is developing its academic programs.",
            height=180,
        )

    if st.button("Compare texts", type="primary"):
        result = compare_texts(reference, hypothesis).to_dict()
        metric_columns = st.columns(5)
        labels = [
            ("Reference tokens", result["reference_tokens"]),
            ("Submission tokens", result["hypothesis_tokens"]),
            ("Edit distance", result["edit_distance"]),
            ("Edit ratio", f'{result["edit_ratio"]:.3f}'),
            ("Length ratio", f'{result["length_ratio"]:.3f}'),
        ]
        for column, (label, value) in zip(metric_columns, labels):
            column.metric(label, value)
        st.caption("Edit ratio is the token edit distance divided by the reference token count.")

with corpus_tab:
    uploaded = st.file_uploader("Upload a CSV or JSONL corpus", type=["csv", "jsonl", "ndjson"])
    st.caption("Required columns: record_id, task_category, source_text, mt_output, student_submission.")

    if uploaded is not None:
        suffix = Path(uploaded.name).suffix.lower()
        try:
            if suffix == ".csv":
                raw_df = pd.read_csv(uploaded)
            else:
                raw_df = pd.read_json(uploaded, lines=True)

            st.subheader("Input preview")
            st.dataframe(raw_df.head(20), use_container_width=True, hide_index=True)

            required = {"record_id", "task_category", "source_text", "mt_output", "student_submission"}
            missing = sorted(required.difference(raw_df.columns))
            if missing:
                st.error("Missing required columns: " + ", ".join(missing))
            elif st.button("Run corpus analysis", type="primary"):
                with tempfile.TemporaryDirectory() as temp_dir:
                    input_path = Path(temp_dir) / ("corpus.csv" if suffix == ".csv" else "corpus.jsonl")
                    if suffix == ".csv":
                        raw_df.to_csv(input_path, index=False)
                    else:
                        raw_df.to_json(input_path, orient="records", lines=True, force_ascii=False)

                    corpus_df = compute_record_metrics(load_corpus(input_path))

                summary = summarize_corpus(corpus_df)
                st.subheader("Corpus summary")
                summary_columns = st.columns(3)
                summary_columns[0].metric("Records", summary["number_of_records"])
                summary_columns[1].metric("Students", summary["number_of_students"] or "Not provided")
                summary_columns[2].metric("Exercises", summary["number_of_exercises"] or "Not provided")
                st.json(summary)

                st.subheader("Computed metrics")
                st.dataframe(corpus_df.head(100), use_container_width=True, hide_index=True)

                descriptives = group_descriptives(corpus_df)
                if not descriptives.empty:
                    st.subheader("Grouped descriptives")
                    st.dataframe(descriptives, use_container_width=True)

                csv_data = corpus_df.to_csv(index=False).encode("utf-8-sig")
                st.download_button(
                    "Download analysed corpus CSV",
                    csv_data,
                    "arabicedunlp_analysed_corpus.csv",
                    "text/csv",
                )
                st.download_button(
                    "Download summary JSON",
                    json.dumps(summary, ensure_ascii=False, indent=2).encode("utf-8"),
                    "arabicedunlp_summary.json",
                    "application/json",
                )
        except Exception as exc:
            st.error(f"Analysis could not be completed: {exc}")
