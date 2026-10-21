from pathlib import Path

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
VALID_SPLITS = {"train", "test"}


def load_ultrasound_dataset(root="data/raw/ultrasound/data"):
    """Return valid image paths and their folder-derived labels."""
    root = Path(root)

    if not root.is_dir():
        raise FileNotFoundError(f"Dataset directory not found: {root}")

    records = []

    for split in sorted(VALID_SPLITS):
        split_dir = root / split

        if not split_dir.is_dir():
            raise FileNotFoundError(f"Missing dataset split: {split_dir}")

        for class_dir in sorted(p for p in split_dir.iterdir() if p.is_dir()):
            for path in sorted(class_dir.rglob("*")):
                if not path.is_file() or path.suffix.lower() not in IMAGE_EXTENSIONS:
                    continue

                # Skip zero-byte files; image decoding is checked separately.
                if path.stat().st_size == 0:
                    continue

                records.append({
                    "path": path,
                    "split": split,
                    "label": class_dir.name,
                })

    return records


if __name__ == "__main__":
    records = load_ultrasound_dataset()

    for split in sorted(VALID_SPLITS):
        split_records = [r for r in records if r["split"] == split]
        print(f"\n{split.upper()}: {len(split_records)} valid images")

        labels = sorted({r["label"] for r in split_records})
        for label in labels:
            count = sum(r["label"] == label for r in split_records)
            print(f"  {label}: {count}")

    print(f"\nTotal valid images: {len(records)}")
    print("Note: labels are folder names, not verified clinical diagnoses.")
