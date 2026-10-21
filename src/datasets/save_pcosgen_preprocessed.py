
from pathlib import Path
import pandas as pd
from PIL import Image

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed" / "ultrasound" / "pcosgen"
MANIFEST_PATH = PROCESSED_DIR / "manifest.csv"
OUTPUT_DIR = PROCESSED_DIR / "images"
IMAGE_SIZE = (224, 224)


def main():
    if not MANIFEST_PATH.exists():
        raise FileNotFoundError(f"Manifest not found: {MANIFEST_PATH}")

    manifest = pd.read_csv(MANIFEST_PATH)

    if "path" not in manifest.columns:
        raise ValueError("Manifest must contain a 'path' column.")
    if manifest.empty:
        raise ValueError("Manifest contains no image records.")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    total = len(manifest)
    print(f"Preprocessing {total} images...")

    for index, row in manifest.iterrows():
        source_path = Path(row["path"])

        if not source_path.is_file():
            raise FileNotFoundError(f"Source image not found: {source_path}")

        output_path = OUTPUT_DIR / f"{index:04d}_{source_path.stem}.png"

        with Image.open(source_path) as image:
            image = image.convert("L")
            image = image.resize(IMAGE_SIZE, Image.Resampling.BILINEAR)
            image.save(output_path, format="PNG")

        if (index + 1) % 200 == 0 or index + 1 == total:
            print(f"Processed {index + 1}/{total}")

    print("\nPreprocessing complete!")
    print(f"Saved images to: {OUTPUT_DIR}")
    print(f"Total images processed: {total}")


if __name__ == "__main__":
    main()
