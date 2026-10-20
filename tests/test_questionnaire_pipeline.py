
from pathlib import Path

import pandas as pd
from pandas.testing import assert_frame_equal

from src.preprocessing.questionnaire import clean_questionnaire


ROOT = Path(__file__).resolve().parents[1]

RAW_PATH = (
    ROOT
    / "data"
    / "raw"
    / "questionnaire"
    / "CLEAN- PCOS SURVEY SPREADSHEET.csv"
)

PROCESSED_PATH = (
    ROOT / "data" / "processed" / "questionnaire_cleaned.csv"
)


def standardize_columns(df):
    """Normalize line breaks and whitespace in column names."""
    df = df.copy()
    df.columns = (
        df.columns
        .str.replace(r"[\r\n]+", " ", regex=True)
        .str.strip()
    )
    return df


def test_raw_dataset_is_unchanged_and_has_expected_shape():
    raw = pd.read_csv(RAW_PATH)

    assert raw.shape == (465, 16)
    assert raw.columns.is_unique


def test_cleaned_dataset_has_expected_shape():
    raw = pd.read_csv(RAW_PATH)
    cleaned = pd.read_csv(PROCESSED_PATH)

    expected_columns = standardize_columns(raw).columns

    assert cleaned.shape == (464, 16)
    assert list(cleaned.columns) == list(expected_columns)


def test_preprocessing_removes_exact_duplicates():
    raw = pd.read_csv(RAW_PATH)
    cleaned = pd.read_csv(PROCESSED_PATH)

    expected = (
        standardize_columns(raw)
        .drop_duplicates()
        .reset_index(drop=True)
    )
    actual = cleaned.reset_index(drop=True)

    assert len(raw) - len(expected) == 1

    assert_frame_equal(
        actual,
        expected,
        check_dtype=False,
    )


def test_cleaned_dataset_has_no_duplicates_or_missing_values():
    cleaned = pd.read_csv(PROCESSED_PATH)

    assert not cleaned.duplicated().any()
    assert not cleaned.isna().any().any()


def test_diagnosis_counts_are_preserved_after_deduplication():
    raw = pd.read_csv(RAW_PATH)
    cleaned = pd.read_csv(PROCESSED_PATH)

    raw_target = next(
        c for c in raw.columns
        if "PCOS/PCOD" in c
    )
    cleaned_target = next(
        c for c in cleaned.columns
        if "PCOS/PCOD" in c
    )

    expected = (
        raw.drop_duplicates()[raw_target]
        .value_counts()
        .sort_index()
    )
    actual = (
        cleaned[cleaned_target]
        .value_counts()
        .sort_index()
    )

    assert_frame_equal(
        actual.to_frame(),
        expected.to_frame(),
        check_dtype=False,
    )


def test_pipeline_generates_expected_cleaned_dataset(tmp_path):
    output_path = tmp_path / "questionnaire_cleaned.csv"

    result = clean_questionnaire(RAW_PATH, output_path)

    expected = (
        standardize_columns(pd.read_csv(RAW_PATH))
        .drop_duplicates()
        .reset_index(drop=True)
    )

    assert output_path.exists()
    assert result.shape == (464, 16)
    assert not result.duplicated().any()
    assert not result.isna().any().any()

    assert_frame_equal(
        result.reset_index(drop=True),
        expected,
        check_dtype=False,
    )

    saved = pd.read_csv(output_path)

    assert_frame_equal(
        result.reset_index(drop=True),
        saved.reset_index(drop=True),
        check_dtype=False,
    )
