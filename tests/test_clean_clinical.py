
import pandas as pd
import pytest

from scripts.clean_clinical import clean_dataframe, TARGET, BP_COLUMNS


@pytest.fixture
def sample_data():
    return pd.DataFrame({
        "Sl. No": [1, 2, 3],
        "Patient File No.": ["P001", "P002", "P003"],
        TARGET: [1, 0, 1],
        "AMH(ng/mL)": ["5.2", "invalid", "3.1"],
        BP_COLUMNS[0]: [120, 40, 110],
        BP_COLUMNS[1]: [80, 35, 70],
        "Unnamed: 44": [None, None, None],
    })


def test_removes_identifiers_and_empty_column(sample_data):
    cleaned = clean_dataframe(sample_data)

    assert "Sl. No" not in cleaned.columns
    assert "Patient File No." not in cleaned.columns
    assert "Unnamed: 44" not in cleaned.columns


def test_converts_invalid_numeric_values_to_missing(sample_data):
    cleaned = clean_dataframe(sample_data)

    assert pd.isna(cleaned.loc[1, "AMH(ng/mL)"])


def test_marks_suspicious_blood_pressure_as_missing(sample_data):
    cleaned = clean_dataframe(sample_data)

    assert pd.isna(cleaned.loc[1, BP_COLUMNS[0]])
    assert pd.isna(cleaned.loc[1, BP_COLUMNS[1]])

    # Valid readings should remain unchanged.
    assert cleaned.loc[0, BP_COLUMNS[0]] == 120
    assert cleaned.loc[0, BP_COLUMNS[1]] == 80


def test_target_is_integer(sample_data):
    cleaned = clean_dataframe(sample_data)

    assert str(cleaned[TARGET].dtype) == "int64"
    assert cleaned[TARGET].tolist() == [1, 0, 1]


def test_rejects_invalid_target_labels(sample_data):
    sample_data.loc[0, TARGET] = 2

    with pytest.raises(ValueError, match="Unexpected PCOS target values"):
        clean_dataframe(sample_data)


def test_rejects_missing_required_columns(sample_data):
    sample_data.drop(columns=["AMH(ng/mL)"], inplace=True)

    with pytest.raises(ValueError, match="Required columns are missing"):
        clean_dataframe(sample_data)


def test_drops_rows_with_missing_target(sample_data):
    sample_data.loc[1, TARGET] = None

    cleaned = clean_dataframe(sample_data)

    assert len(cleaned) == 2
    assert cleaned[TARGET].tolist() == [1, 1]


def test_rejects_nonempty_unnamed_column(sample_data):
    sample_data.loc[0, "Unnamed: 44"] = "unexpected data"

    with pytest.raises(ValueError, match="contains data"):
        clean_dataframe(sample_data)
