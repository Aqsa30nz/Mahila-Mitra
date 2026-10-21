
from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATASET_DIR = PROJECT_ROOT / "data" / "raw" / "ultrasound" / "pcosgen"
IMAGE_DIR = DATASET_DIR / "images"
LABEL_FILE = DATASET_DIR / "class_label.xlsx"

OUTPUT_DIR = (
    PROJECT_ROOT / "data" / "processed" / "ultrasound" / "pcosgen"
)

RANDOM_SEED = 42
VALIDATION_SIZE = 0.20


def find_column(columns, required_phrases):
    matches = [
        column
        for column in columns
        if all(phrase in column.lower() for phrase in required_phrases)
    ]

    if len(matches) != 1:
        raise ValueError(
            f"Could not uniquely identify column containing "
            f"{required_phrases}. Available columns: {list(columns)}"
        )

    return matches[0]


def main():
    if not IMAGE_DIR.is_dir():
        raise FileNotFoundError(f"Image folder not found: {IMAGE_DIR}")

    if not LABEL_FILE.is_file():
        raise FileNotFoundError(f"Excel label file not found: {LABEL_FILE}")

    df = pd.read_excel(LABEL_FILE)
    df.columns = [str(column).strip() for column in df.columns]

    image_column = find_column(df.columns, ["imagepath"])

    abnormality_column = find_column(
        df.columns,
        ["ultrasound images", "normal or has some abnormality"],
    )

    pco_column = find_column(
        df.columns,
        ["polycsytic ovary", "visible or not visible"],
    )

    df = df.dropna(subset=[image_column]).copy()
    df[image_column] = df[image_column].astype(str).str.strip()
    df = df[df[image_column] != ""].copy()

    if df[image_column].duplicated().any():
        duplicates = df.loc[
            df[image_column].duplicated(), image_column
        ].tolist()
        raise ValueError(f"Duplicate image filenames found: {duplicates[:10]}")

    df["path"] = df[image_column].apply(
        lambda name: str((IMAGE_DIR / name).resolve())
    )

    missing = df.loc[
        ~df["path"].apply(lambda path: Path(path).is_file()),
        image_column,
    ].tolist()

    if missing:
        raise FileNotFoundError(
            f"{len(missing)} images are missing. Examples: {missing[:10]}"
        )

    label_mapping = {
        "appears normal": 0,
        "appears abnormal": 1,
    }

    df["abnormality_label_original"] = df[abnormality_column]
    df["pco_visibility_label_original"] = df[pco_column]

    normalized_labels = (
        df[abnormality_column].astype(str).str.strip().str.lower()
    )

    df["label"] = normalized_labels.map(label_mapping)

    if df["label"].isna().any():
        unknown = sorted(
            normalized_labels[df["label"].isna()].unique().tolist()
        )
        raise ValueError(
            f"Unexpected abnormality labels found: {unknown}"
        )

    manifest = df[
        [
            image_column,
            "path",
            "abnormality_label_original",
            "pco_visibility_label_original",
            "label",
        ]
    ].rename(columns={image_column: "imagePath"})

    train_df, validation_df = train_test_split(
        manifest,
        test_size=VALIDATION_SIZE,
        random_state=RANDOM_SEED,
        stratify=manifest["label"],
    )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    manifest.to_csv(OUTPUT_DIR / "manifest.csv", index=False)
    train_df.to_csv(OUTPUT_DIR / "train.csv", index=False)
    validation_df.to_csv(OUTPUT_DIR / "validation.csv", index=False)

    print("PCOSGen dataset preparation successful.")
    print(f"Total images: {len(manifest)}")
    print(f"Training images: {len(train_df)}")
    print(f"Validation images: {len(validation_df)}")
    print("\nAll-image label counts:")
    print(manifest["label"].value_counts().sort_index())
    print("\nTraining label counts:")
    print(train_df["label"].value_counts().sort_index())
    print("\nValidation label counts:")
    print(validation_df["label"].value_counts().sort_index())
    print(f"\nOutput folder: {OUTPUT_DIR}")
    print(
        "\nImportant: labels represent ultrasound appearance "
        "(normal/abnormal), not a confirmed clinical PCOS diagnosis."
    )


if __name__ == "__main__":
    main()
