
from pathlib import Path
import pandas as pd

DATA_DIR = Path("data/processed/ultrasound/pcosgen")

original = pd.read_csv(DATA_DIR / "manifest.csv")
processed = pd.read_csv(DATA_DIR / "manifest_preprocessed.csv")
train = pd.read_csv(DATA_DIR / "train_preprocessed.csv")
validation = pd.read_csv(DATA_DIR / "validation_preprocessed.csv")

# Verify that preprocessing did not change the original labels.
check = original[["imagePath", "label"]].merge(
    processed[["imagePath", "label", "processed_path"]],
    on="imagePath",
    how="outer",
    suffixes=("_original", "_processed"),
    indicator=True,
)

print("Total original rows:", len(original))
print("Total processed rows:", len(processed))
print("Train rows:", len(train))
print("Validation rows:", len(validation))
print("Unmatched original/processed rows:", (check["_merge"] != "both").sum())
print(
    "Label mismatches:",
    (check["label_original"] != check["label_processed"]).sum()
)
print("Missing processed paths:", processed["processed_path"].isna().sum())

print("\nFull dataset label counts:")
print(processed["label"].value_counts().sort_index())

print("\nTrain label counts:")
print(train["label"].value_counts().sort_index())

print("\nValidation label counts:")
print(validation["label"].value_counts().sort_index())

assert len(original) == 3200
assert len(processed) == 3200
assert len(train) == 2560
assert len(validation) == 640
assert (check["_merge"] == "both").all()
assert (check["label_original"] == check["label_processed"]).all()
assert processed["processed_path"].notna().all()
assert processed["processed_path"].map(lambda p: Path(p).is_file()).all()

print("\nALL MANIFEST CHECKS PASSED")
