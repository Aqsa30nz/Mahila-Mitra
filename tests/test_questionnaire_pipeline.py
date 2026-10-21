from pathlib import Path

import pandas as pd
from pandas.testing import assert_frame_equal
from src.preprocessing.demo import format_answer
from src.preprocessing.questionnaire import clean_questionnaire


def make_raw_dataset(path: Path) -> pd.DataFrame:
    """Create messy headers, distinct records, and one exact duplicate."""
    df = pd.DataFrame(
        {
            " Age\n": [21, 22, 23, 21],
            "Have you been diagnosed with PCOS/PCOD? ": [1, 0, 1, 1],
            "Weight (kg)": [60, 55, 65, 60],
        }
    )
    df.to_csv(path, index=False)
    return df


def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Apply the pipeline's documented header normalization."""
    df = df.copy()
    df.columns = (
        df.columns
        .str.replace(r"[\r\n]+", " ", regex=True)
        .str.strip()
    )
    return df


def test_raw_dataset_is_unchanged(tmp_path):
    raw_path = tmp_path / "raw.csv"
    original = make_raw_dataset(raw_path)
    original_bytes = raw_path.read_bytes()

    output_path = tmp_path / "processed" / "cleaned.csv"
    clean_questionnaire(raw_path, output_path)

    assert raw_path.read_bytes() == original_bytes
    assert_frame_equal(
        pd.read_csv(raw_path),
        original,
        check_dtype=False,
    )


def test_cleaned_dataset_has_expected_shape_and_headers(tmp_path):
    raw_path = tmp_path / "raw.csv"
    make_raw_dataset(raw_path)

    cleaned = clean_questionnaire(raw_path, tmp_path / "cleaned.csv")

    assert cleaned.shape == (3, 3)
    assert list(cleaned.columns) == [
        "Age",
        "Have you been diagnosed with PCOS/PCOD?",
        "Weight (kg)",
    ]


def test_preprocessing_removes_exact_duplicates(tmp_path):
    raw_path = tmp_path / "raw.csv"
    raw = make_raw_dataset(raw_path)

    output_path = tmp_path / "cleaned.csv"
    actual = clean_questionnaire(raw_path, output_path)

    expected = (
        standardize_columns(raw)
        .drop_duplicates()
        .reset_index(drop=True)
    )

    assert len(raw) - len(expected) == 1
    assert_frame_equal(
        actual.reset_index(drop=True),
        expected,
        check_dtype=False,
    )


def test_cleaned_dataset_has_no_duplicates(tmp_path):
    raw_path = tmp_path / "raw.csv"
    make_raw_dataset(raw_path)

    cleaned = clean_questionnaire(raw_path, tmp_path / "cleaned.csv")

    assert not cleaned.duplicated().any()
    assert not cleaned.isna().any().any()


def test_diagnosis_counts_are_preserved_after_deduplication(tmp_path):
    raw_path = tmp_path / "raw.csv"
    raw = make_raw_dataset(raw_path)

    cleaned = clean_questionnaire(raw_path, tmp_path / "cleaned.csv")

    target = "Have you been diagnosed with PCOS/PCOD?"

    expected_counts = (
        standardize_columns(raw)
        .drop_duplicates()[target]
        .value_counts()
        .sort_index()
    )
    actual_counts = cleaned[target].value_counts().sort_index()

    assert_frame_equal(
        actual_counts.to_frame(),
        expected_counts.to_frame(),
        check_dtype=False,
    )


def test_pipeline_saves_output_and_creates_parent_directory(tmp_path):
    raw_path = tmp_path / "raw.csv"
    make_raw_dataset(raw_path)

    output_path = tmp_path / "new_directory" / "cleaned.csv"
    result = clean_questionnaire(raw_path, output_path)

    assert output_path.exists()

    saved = pd.read_csv(output_path)
    assert_frame_equal(
        result.reset_index(drop=True),
        saved.reset_index(drop=True),
        check_dtype=False,
    )


def test_pipeline_preserves_distinct_rows_with_same_diagnosis(tmp_path):
    raw_path = tmp_path / "raw.csv"
    make_raw_dataset(raw_path)

    cleaned = clean_questionnaire(raw_path, tmp_path / "cleaned.csv")

    target = "Have you been diagnosed with PCOS/PCOD?"

    # Distinct records sharing a diagnosis value must both be retained.
    assert (cleaned[target] == 1).sum() == 2
    assert (cleaned[target] == 0).sum() == 1


def test_demo_preserves_unverified_binary_codes():
    question = "Have you been diagnosed with PCOS/PCOD?"

    assert format_answer(question, 0) == "0"
    assert format_answer(question, 1) == "1"
    assert format_answer(question, 0.0) == "0"
    assert format_answer(question, 1.0) == "1"
    assert format_answer(question, float("nan")) == "Not provided"
