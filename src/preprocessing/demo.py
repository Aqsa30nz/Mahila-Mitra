
from pathlib import Path
import pandas as pd

from src.preprocessing.questionnaire import clean_questionnaire

ROOT = Path(__file__).resolve().parents[2]

RAW_FILE = (
    ROOT / "data" / "raw" / "questionnaire"
    / "CLEAN- PCOS SURVEY SPREADSHEET.csv"
)
CLEAN_FILE = ROOT / "data" / "processed" / "questionnaire_cleaned.csv"

BINARY_COLUMNS = {
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
}


def format_answer(question, answer):
    if pd.isna(answer):
        return "Not provided"

    if question in BINARY_COLUMNS:
        try:
            value = float(answer)
            if value == 0:
                return "No"
            if value == 1:
                return "Yes"
        except (ValueError, TypeError):
            pass

    return str(answer)


def main():
    raw = pd.read_csv(RAW_FILE)

    print("=" * 60)
    print("       MAHILA-MITRA: QUESTIONNAIRE PREPROCESSING")
    print("=" * 60)

    print("\n[1] ORIGINAL DATASET")
    print("-" * 40)
    print(f"Rows: {len(raw)}")
    print(f"Columns: {len(raw.columns)}")
    print(f"Exact duplicate rows: {raw.duplicated().sum()}")
    print(f"Missing values: {raw.isna().sum().sum()}")

    print("\n[2] RUNNING PREPROCESSING")
    print("-" * 40)
    print("Standardizing column names...")
    print("Removing exact duplicate records...")
    print("Saving the cleaned dataset...")

    cleaned = clean_questionnaire(RAW_FILE, CLEAN_FILE)

    print("\n[3] PREPROCESSING RESULTS")
    print("-" * 40)
    print(f"Original shape: {raw.shape}")
    print(f"Cleaned shape:  {cleaned.shape}")
    print(f"Records removed: {len(raw) - len(cleaned)}")
    print(f"Duplicates remaining: {cleaned.duplicated().sum()}")
    print(f"Missing values remaining: {cleaned.isna().sum().sum()}")

    normalized_columns = (
        pd.Index(raw.columns.astype(str))
        .str.replace(r"[\r\n]+", " ", regex=True)
        .str.strip()
    )
    print(
        "Columns preserved: "
        f"{list(normalized_columns) == list(cleaned.columns)}"
    )
    print(f"Saved output: {CLEAN_FILE.relative_to(ROOT)}")

    print("\n[4] SAMPLE RECORD: QUESTION AND ANSWER")
    print("-" * 40)

    if not cleaned.empty:
        sample = cleaned.iloc[0]

        for question, answer in sample.items():
            print(f"\nQuestion/field: {question}")
            print(f"Recorded answer: {format_answer(question, answer)}")

    print("\n[5] FINAL VERIFICATION")
    print("-" * 40)

    saved = pd.read_csv(CLEAN_FILE)

    print(f"Saved dataset shape: {saved.shape}")
    print(f"Saved file has duplicates: {saved.duplicated().any()}")
    print(f"Saved file has missing values: {saved.isna().any().any()}")
    print(f"Output file exists: {CLEAN_FILE.exists()}")

    print("\nDemo completed.")
    print("Note: This is preprocessing, not a PCOS prediction.")
    print("=" * 60)


if __name__ == "__main__":
    main()
