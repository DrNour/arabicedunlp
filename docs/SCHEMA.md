# Corpus Schema

ArabicEduNLP expects a row-level corpus where each row represents one translation or post-editing record.

## Required columns

| Column | Type | Description |
|---|---:|---|
| `record_id` | string | Unique record identifier |
| `task_category` | string | Normalised category, e.g. `translation` or `post_editing` |
| `source_text` | string | Source text used in the exercise |
| `mt_output` | string | MT output or comparison baseline |
| `student_submission` | string | Student visible submission or final edited text |

## Recommended columns

| Column | Type | Description |
|---|---:|---|
| `student_id` | string | Anonymised student identifier |
| `exercise_id` | integer/string | Exercise identifier |
| `task_type` | string | Original task label |
| `student_submission_view` | string | `final_submission` or `track_changes_report` |
| `time_spent_sec` | float | Time spent in seconds |
| `preferred_edit_count` | integer/float | Preferred edit count from exported or reconstructed report |
| `preferred_edit_source` | string | Source of preferred edit count |
| `warning` | string | Warning generated during extraction |
| `notes` | string | Free notes |

## Generated columns

ArabicEduNLP can generate these columns:

| Column | Description |
|---|---|
| `computed_source_word_count` | Token count of source text |
| `computed_mt_word_count` | Token count of MT output |
| `computed_submission_word_count` | Token count of student submission |
| `computed_mt_visible_submission_edit_distance` | Token-level MT-to-submission Levenshtein distance |
| `computed_mt_visible_submission_edit_ratio` | Edit distance divided by MT token count |
| `computed_visible_length_ratio` | Submission token count divided by MT token count |

## Ethical note

The private classroom corpus should not be committed to a public repository unless it is fully anonymised and cleared for release. The public repository should include synthetic data or a small consent-cleared sample.
