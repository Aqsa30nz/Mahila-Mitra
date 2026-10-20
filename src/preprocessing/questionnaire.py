
from pathlib import Path

import pandas as pd


def clean_questionnaire(
    input_path: Path,
    output_path: Path,
) -> pd.DataFrame:
    """Load, standardize, deduplicate, and save questionnaire data."""

    input_path = Path(input_path)
    output_path = Path(output_path)

    df = pd.read_csv(input_path)

    # Standardize line breaks and whitespace in column names.
    df.columns = (
        df.columns
        .str.replace(r"[\r\n]+", " ", regex=True)
        .str.strip()
    )

    # Keep the original input file unchanged.
    df_clean = df.drop_duplicates().copy()

    # Create the output directory and save the cleaned dataset.
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df_clean.to_csv(output_path, index=False)

    return df_clean

