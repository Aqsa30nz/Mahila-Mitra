
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
    """Validate and clean the clinical dataset without modifying the source."""

    df = df.copy()

    # Normalize surrounding whitespace in column names first.
    df.columns = df.columns.str.strip()

    # Validate required columns.
    missing_columns = [
        column for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]
    if missing_columns:
        raise ValueError(
            f"Required columns are missing: {missing_columns}"
        )

    # Inspect the unexpected export column before dropping it.
    if "Unnamed: 44" in df.columns:
        extra = df["Unnamed: 44"]
        non_missing = extra.dropna()

        if not non_missing.empty:
            print(
                "Inspecting Unnamed: 44:",
                non_missing.value_counts(dropna=False).to_dict(),
            )

            # Permit only the verified placeholder and duplicate value.
            for idx, value in non_missing.items():
                if isinstance(value, str) and value.strip() == ".":
                    continue

                # FIX: Do not access a column that may not exist in a test
                # sample. Without it, the extra value cannot be verified.
                if "Endometrium (mm)" not in df.columns:
                    raise ValueError(
                        "'Unnamed: 44' contains data that cannot be verified."
                    )

                endometrium = df.loc[idx, "Endometrium (mm)"]
                numeric_value = pd.to_numeric(
                    pd.Series([value]), errors="coerce"
                ).iloc[0]

                if (
                    pd.notna(endometrium)
                    and pd.notna(numeric_value)
                    and numeric_value == endometrium
                ):
                    continue

                raise ValueError(
                    "'Unnamed: 44' contains unexpected data. "
                    "Inspect it before dropping."
                )

        df = df.drop(columns=["Unnamed: 44"])

    # Remove identifier columns from the modelling dataset.
    identifier_columns = ["Sl. No", "Patient File No."]
    df = df.drop(
        columns=[
            column for column in identifier_columns
            if column in df.columns
        ]
    )

    # Correct the single verified trailing-period typo in the source.
    beta_hcg_ii = "II    beta-HCG(mIU/mL)"
    if beta_hcg_ii in df.columns:
        values = df[beta_hcg_ii].astype("string").str.strip()
        df[beta_hcg_ii] = values.mask(values.eq("1.99."), "1.99")

    # Validate the target labels before removing rows with missing targets.
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

    # Convert selected clinical measurements to numeric values.
    # Invalid entries become missing rather than being silently guessed.
    numeric_columns = [
        "AMH(ng/mL)",
        *BP_COLUMNS,
        beta_hcg_ii,
    ]
    for column in numeric_columns:
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce")

    # Flag project-specific suspicious low blood-pressure readings.
    systolic = BP_COLUMNS[0]
    diastolic = BP_COLUMNS[1]

    low_systolic = df[systolic].notna() & (df[systolic] < 50)
    low_diastolic = df[diastolic].notna() & (df[diastolic] < 40)

    print(
        "Suspicious low systolic BP readings:",
        int(low_systolic.sum()),
    )
    print(
        "Suspicious low diastolic BP readings:",
        int(low_diastolic.sum()),
    )

    # These are project-specific screening thresholds, not universal
    # clinical rules. Mark the suspicious measurements as missing.
    df.loc[low_systolic, systolic] = float("nan")
    df.loc[low_diastolic, diastolic] = float("nan")

    return df


def main(
    source: Path = SOURCE,
    output: Path = OUTPUT,
) -> None:
    """Read the source workbook, clean it, and save the cleaned CSV."""

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
