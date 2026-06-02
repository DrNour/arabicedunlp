# ArabicEduNLP

ArabicEduNLP is a lightweight Python package for **Arabic translation and post-editing analytics**. It is designed for applied NLP research on Arabic/English classroom corpora, MT output, student submissions, and post-editing records.

The package supports the manuscript:

> *ArabicEduNLP: A Corpus-Driven NLP Framework for Arabic Translation and Post-Editing Analytics*

## What the package does

ArabicEduNLP provides transparent, reproducible utilities for:

- Arabic text normalization;
- Arabic/English word tokenization;
- token-level Levenshtein edit distance;
- MT-to-submission edit-ratio calculation;
- corpus loading from CSV or JSONL;
- grouped descriptive summaries for translation and post-editing records;
- command-line corpus analysis.

It is **not** intended to replace broad Arabic NLP toolkits such as CAMeL Tools. Instead, it complements them by focusing on view-aware translation-process analytics and post-editing metrics.

## Installation

```bash
pip install -e .
```

For development:

```bash
pip install -e ".[dev,analysis]"
```

## Quick start

```python
from arabicedunlp import normalize_arabic, word_tokenize, compare_texts

text = "إِنَّ الطُّلَّابَ يَدْرُسُونَ التَّرْجَمَةَ الآلِيَّة."
print(normalize_arabic(text))
print(word_tokenize(text))

result = compare_texts(
    "The university develops its programmes.",
    "The university is developing its academic programmes."
)
print(result.to_dict())
```

## Command-line use

Compare two texts:

```bash
arabicedunlp compare "The university develops programmes." "The university develops academic programmes."
```

Analyze the synthetic sample corpus:

```bash
arabicedunlp analyze data/sample_corpus_synthetic.csv --out outputs/sample_report.json --descriptives outputs/sample_descriptives.csv
```

## Reproducing paper tables

The repository includes a script for reproducing core descriptive tables from a compatible corpus file:

```bash
python scripts/reproduce_paper_tables.py --input data/sample_corpus_synthetic.csv --outdir outputs
```

To reproduce the manuscript tables from the private classroom corpus, place the full CSV at a local path and run:

```bash
python scripts/reproduce_paper_tables.py --input /path/to/corpus_from_docx.csv --outdir outputs/full_corpus
```

The public repository should normally include only synthetic or anonymised data. Student text and identifiers should not be released without appropriate ethical clearance.

## Expected corpus columns

Minimum required columns:

| Column | Description |
|---|---|
| `record_id` | Unique record identifier |
| `task_category` | `translation`, `post_editing`, or another category |
| `source_text` | Original source text |
| `mt_output` | Machine translation output or comparison baseline |
| `student_submission` | Student translation/post-edited text |

Recommended metadata columns:

| Column | Description |
|---|---|
| `student_id` | Anonymised student identifier |
| `exercise_id` | Exercise/task number |
| `student_submission_view` | `final_submission` or `track_changes_report` |
| `time_spent_sec` | Time-on-task in seconds |
| `preferred_edit_count` | Preferred edit count from track changes or exported report |

See `docs/SCHEMA.md` for details.

## Repository structure

```text
src/arabicedunlp/       Python package
data/                   Synthetic sample data and schema
scripts/                Reproducibility scripts
paper_assets/           Aggregate tables derived from the uploaded corpus
docs/                   Architecture, schema, and submission notes
tests/                  Unit tests
```

## Citation

If you use this package, please cite the accompanying manuscript or use the metadata in `CITATION.cff`.

## License

MIT License. See `LICENSE`.
