
from pathlib import Path

import pandas as pd


SOURCE = Path("data/raw/clinical/PCOS_data_without_infertility.xlsx")
OUTPUT = Path("data/processed/clinical_cleaned.csv")
SHEET_NAME = "Full_new"
TARGET = "PCOS (Y/N)"

BP_COLUMNS = [
    "BP _Systolic (mmHg)",
    "BP _Diastolic (mmHg)",
]

REQUIRED_COLUMNS = [
    TARGET,
    "AMH(ng/mL)",
    *BP_COLUMNS,
]


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Validate and clean a clinical dataset without modifying the input."""

    df = df.copy()

    missing_columns = [
        column for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]
    if missing_columns:
        raise ValueError(
            f"Required columns are missing: {missing_columns}"
        )

    # Drop the unnamed column only when it contains no data.
    if "Unnamed: 44" in df.columns:
        if df["Unnamed: 44"].notna().any():
            raise ValueError(
                "'Unnamed: 44' contains data. Inspect it before dropping."
            )
        df = df.drop(columns=["Unnamed: 44"])

    # Remove identifiers from the modelling dataset.
    identifier_columns = ["Sl. No", "Patient File No."]
    df = df.drop(
        columns=[
            column for column in identifier_columns
            if column in df.columns
        ]
    )

    # Validate target labels before excluding rows without labels.
    df[TARGET] = pd.to_numeric(df[TARGET], errors="raise")

    invalid_labels = (
        df[TARGET].notna()
        & ~df[TARGET].isin([0, 1])
    )
    if invalid_labels.any():
        values = sorted(
            df.loc[invalid_labels, TARGET].unique().tolist()
        )
        raise ValueError(f"Unexpected PCOS target values: {values}")

    missing_target_rows = int(df[TARGET].isna().sum())
    if missing_target_rows:
        print(
            "Rows excluded because the target label is missing:",
            missing_target_rows,
        )
        df = df.dropna(subset=[TARGET]).copy()

    df[TARGET] = df[TARGET].astype("int64")

    # Convert invalid AMH and blood-pressure entries to missing values.
    for column in ["AMH(ng/mL)", *BP_COLUMNS]:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    systolic = BP_COLUMNS[0]
    diastolic = BP_COLUMNS[1]

    low_systolic = df[systolic].notna() & (df[systolic] < 50)
    low_diastolic = df[diastolic].notna() & (df[diastolic] < 40)

    print("Suspicious low systolic BP readings:", int(low_systolic.sum()))
    print("Suspicious low diastolic BP readings:", int(low_diastolic.sum()))

    # Project-specific thresholds, not universal clinical rules.
    df.loc[low_systolic, systolic] = float("nan")
    df.loc[low_diastolic, diastolic] = float("nan")

    return df


def main(
    source: Path = SOURCE,
    output: Path = OUTPUT,
) -> None:
    """Read the source workbook, clean it, and save the resulting CSV."""

    source = Path(source)
    output = Path(output)

    if not source.is_file():
        raise FileNotFoundError(
            f"Clinical dataset not found: {source.resolve()}"
        )

    df = pd.read_excel(source, sheet_name=SHEET_NAME)
    original_rows = len(df)

    cleaned = clean_dataframe(df)

    output.parent.mkdir(parents=True, exist_ok=True)
    cleaned.to_csv(output, index=False)

    print("\nClinical preprocessing complete.")
    print("Input:", source)
    print("Output:", output)
    print("Original rows:", original_rows)
    print("Output rows:", len(cleaned))
    print("Columns:", len(cleaned.columns))

    print("\nMissing values by column:")
    missing = cleaned.isna().sum()
    print(missing[missing > 0].to_string() or "None")

    print("\nPCOS target distribution:")
    print(cleaned[TARGET].value_counts().sort_index().to_string())


if __name__ == "__main__":
    main()
