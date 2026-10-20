
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]

RAW = (
    ROOT / "data" / "raw" / "questionnaire"
    / "CLEAN- PCOS SURVEY SPREADSHEET.csv"
)
REPORT_DIR = ROOT / "reports"


def main():
    df = pd.read_csv(RAW)
    original_rows = len(df)

    # Standardize headers for checking; raw file is not modified.
    df.columns = (
        df.columns.astype(str)
        .str.replace(r"[\r\n]+", " ", regex=True)
        .str.strip()
    )

    issues = []

    def flag(mask, column, reason):
        for idx in df.index[mask.fillna(False)]:
            issues.append({
                "csv_data_row": int(idx) + 2,
                "column": column,
                "value": df.loc[idx, column],
                "issue": reason,
            })

    # Missing values
    for col in df.columns:
        flag(df[col].isna(), col, "Missing value")

    # Exact duplicate records: report every repeated copy after the first.
    duplicate_mask = df.duplicated(keep="first")
    for idx in df.index[duplicate_mask]:
        issues.append({
            "csv_data_row": int(idx) + 2,
            "column": "(entire row)",
            "value": "Duplicate record",
            "issue": "Exact duplicate of an earlier row",
        })

    # Numeric validation
    numeric_ranges = {
        "Age (in Years)": (10, 100),
        "Weight (in Kg)": (20, 250),
    }

    for col, (low, high) in numeric_ranges.items():
        if col in df.columns:
            values = pd.to_numeric(df[col], errors="coerce")
            flag(values.isna() & df[col].notna(), col, "Not numeric")
            flag(
                values.notna() & ~values.between(low, high),
                col,
                f"Outside broad review range {low}-{high}",
            )

    # Height needs manual unit verification because the survey says
    # "Cm / Feet". Do not automatically convert or replace values.
    height_col = "Height (in Cm / Feet)"
    if height_col in df.columns:
        height = pd.to_numeric(df[height_col], errors="coerce")
        flag(
            height.isna() & df[height_col].notna(),
            height_col,
            "Not numeric",
        )
        flag(
            height.notna() & (height <= 0),
            height_col,
            "Height must be positive",
        )
        flag(
            height.notna() & (height > 0) & (height < 100),
            height_col,
            "Review: may use feet or may be an incorrect entry",
        )
        flag(
            height.notna() & (height > 230),
            height_col,
            "Review: unusually high if interpreted as centimetres",
        )

    # Binary fields: allowed values are provisionally checked as 0/1.
    # This does not confirm which value means Yes or No.
    binary_cols = [
        "Have you gained weight recently?",
        "Do you have excessive body/facial hair growth ?",
        "Are you noticing skin darkening recently?",
        "Do have hair loss/hair thinning/baldness ?",
        "Do you have pimples/acne on your face/jawline ?",
        "Do you eat fast food regularly ?",
        "Do you exercise on a regular basis ?",
        "Have you been diagnosed with PCOS/PCOD?",
        "Do you experience mood swings ?",
        "Are your periods regular ?",
    ]

    for col in binary_cols:
        if col in df.columns:
            values = pd.to_numeric(df[col], errors="coerce")
            flag(
                values.isna() & df[col].notna(),
                col,
                "Expected a numeric binary value",
            )
            flag(
                values.notna() & ~values.isin([0, 1]),
                col,
                "Expected 0 or 1; verify source coding",
            )

    # These fields need their original survey instructions to confirm
    # code meanings and acceptable values.
    review_cols = [
        "Can you tell us your blood group ?",
        "After how many months do you get your periods? (select 1- if every month/regular)",
        "How long does your period last ? (in Days) example- 1,2,3,4.....",
    ]

    for col in review_cols:
        if col in df.columns:
            values = pd.to_numeric(df[col], errors="coerce")
            flag(
                values.isna() & df[col].notna(),
                col,
                "Not numeric; verify against survey options",
            )

    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    issue_df = pd.DataFrame(
        issues,
        columns=["csv_data_row", "column", "value", "issue"],
    )
    issue_path = REPORT_DIR / "questionnaire_validation_issues.csv"
    issue_df.to_csv(issue_path, index=False)

    print("\n=== QUESTIONNAIRE DATA VALIDATION ===")
    print(f"Original rows: {original_rows}")
    print(f"Columns: {df.shape[1]}")
    print(f"Exact duplicate rows: {int(duplicate_mask.sum())}")
    print(f"Missing cells: {int(df.isna().sum().sum())}")
    print(f"Total flagged findings: {len(issue_df)}")
    print(f"Audit report: {issue_path.relative_to(ROOT)}")

    print("\nFindings by issue type:")
    if issue_df.empty:
        print("No issues found by these checks.")
    else:
        print(issue_df["issue"].value_counts().to_string())
        print("\nFirst 15 findings:")
        print(issue_df.head(15).to_string(index=False))

    print("\nRaw dataset was not modified.")
    print("Flagged values require review; they were not auto-corrected.")


if __name__ == "__main__":
    main()
