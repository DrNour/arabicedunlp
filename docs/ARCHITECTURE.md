# ArabicEduNLP Architecture

ArabicEduNLP follows a modular architecture intended for reproducible applied NLP research.

## Pipeline

```text
DOCX/CSV/JSONL records
        |
        v
Corpus loader and schema validation
        |
        v
Arabic/English normalization and tokenization
        |
        v
MT-to-submission comparison
        |
        v
Record-level metrics
        |
        v
Grouped statistical summaries and paper tables
```

## Modules

| Module | Role |
|---|---|
| `normalize.py` | Arabic normalization and diacritic removal |
| `tokenize.py` | Transparent Arabic/English word tokenization |
| `metrics.py` | Levenshtein distance, edit ratio, text comparison |
| `corpus.py` | CSV/JSONL loading, validation, record-level metrics |
| `reporting.py` | Grouped descriptives and JSON reports |
| `cli.py` | Command-line interface |

## Why this architecture?

The package separates linguistic preprocessing from analytics. This is important because Arabic normalization choices can change edit-distance values. The package therefore keeps these choices visible and testable rather than hiding them inside a black-box pipeline.

## Relationship to CAMeL Tools

CAMeL Tools is a broad Arabic NLP toolkit with advanced Arabic processing. ArabicEduNLP is narrower: it uses lightweight, transparent components to support translation-process and post-editing analytics. Future versions can optionally integrate CAMeL Tools for morphology, disambiguation, or dialect-sensitive preprocessing.
