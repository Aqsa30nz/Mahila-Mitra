
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data" / "processed" / "ultrasound" / "pcosgen"
IMAGE_DIR = DATA_DIR / "images"

MANIFEST = DATA_DIR / "manifest.csv"
TRAIN = DATA_DIR / "train.csv"
VALIDATION = DATA_DIR / "validation.csv"


def main():
    manifest = pd.read_csv(MANIFEST)

    required = {"imagePath", "path", "label"}
    if not required.issubset(manifest.columns):
        raise ValueError(f"Manifest needs columns: {required}")

    # The preprocessing script named each image using its manifest row index.
    manifest["processed_path"] = [
        str(IMAGE_DIR / f"{i:04d}_{Path(row['path']).stem}.png")
        for i, (_, row) in enumerate(manifest.iterrows())
    ]

    missing = [
        p for p in manifest["processed_path"]
        if not Path(p).is_file()
    ]
    if missing:
        raise FileNotFoundError(
            f"{len(missing)} processed images are missing. "
            f"Example: {missing[0]}"
        )

    # Save a new full manifest without changing the original.
    manifest.to_csv(DATA_DIR / "manifest_preprocessed.csv", index=False)

    # Match train and validation rows to the full manifest by image filename.
    lookup = manifest.set_index("imagePath")["processed_path"]

    for split_name, source_file in [
        ("train", TRAIN),
        ("validation", VALIDATION),
    ]:
        split = pd.read_csv(source_file)

        if "imagePath" not in split.columns:
            raise ValueError(f"{source_file.name} has no imagePath column")

        split["processed_path"] = split["imagePath"].map(lookup)

        if split["processed_path"].isna().any():
            missing_names = split.loc[
                split["processed_path"].isna(), "imagePath"
            ].tolist()
            raise ValueError(
                f"Could not match {len(missing_names)} images in {split_name}: "
                f"{missing_names[:5]}"
            )

        output = DATA_DIR / f"{split_name}_preprocessed.csv"
        split.to_csv(output, index=False)

        print(f"{output.name}: {len(split)} rows")

    print(f"manifest_preprocessed.csv: {len(manifest)} rows")
    print("All processed paths exist.")
    print("Original CSV files were left unchanged.")


if __name__ == "__main__":
    main()
