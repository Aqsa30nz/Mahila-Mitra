
from pathlib import Path

import pandas as pd
from PIL import Image, ImageOps, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data" / "processed" / "ultrasound" / "pcosgen"
OUTPUT_PATH = ROOT / "outputs" / "pcosgen" / "preprocessing_comparison.png"

manifest = pd.read_csv(DATA_DIR / "manifest_preprocessed.csv")

if manifest.empty:
    raise ValueError("The processed manifest is empty.")

# Select the first record whose original and processed images exist.
record = None
for _, row in manifest.iterrows():
    original_path = Path(row["path"])
    processed_path = Path(row["processed_path"])

    if original_path.is_file() and processed_path.is_file():
        record = row
        break

if record is None:
    raise FileNotFoundError("No matching original/processed image pair found.")

original_path = Path(record["path"])
processed_path = Path(record["processed_path"])

with Image.open(original_path) as image:
    original = image.convert("RGB")

with Image.open(processed_path) as image:
    processed = image.convert("RGB")

# Fit both images into equally sized panels without distorting them.
panel_size = (480, 480)
original_panel = ImageOps.contain(original, panel_size)
processed_panel = ImageOps.contain(processed, panel_size)

canvas = Image.new("RGB", (1040, 600), "white")
draw = ImageDraw.Draw(canvas)

try:
    title_font = ImageFont.truetype("arial.ttf", 24)
    label_font = ImageFont.truetype("arial.ttf", 18)
    detail_font = ImageFont.truetype("arial.ttf", 13)
except OSError:
    title_font = ImageFont.load_default()
    label_font = ImageFont.load_default()
    detail_font = ImageFont.load_default()

draw.text((30, 20), "PCOSGen Ultrasound Preprocessing", fill="black",
          font=title_font)
draw.text((30, 65), "Original image", fill="black", font=label_font)
draw.text((550, 65), "Preprocessed image", fill="black", font=label_font)

canvas.paste(original_panel, (30, 100))
canvas.paste(processed_panel, (550, 100))

draw.text(
    (30, 590 - 20),
    f"Original: {original.size[0]} x {original.size[1]} pixels",
    fill="black",
    font=detail_font,
)
draw.text(
    (550, 590 - 20),
    "Grayscale conversion + bilinear resize + PNG saving",
    fill="black",
    font=detail_font,
)

OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
canvas.save(OUTPUT_PATH)

print("Comparison saved to:", OUTPUT_PATH)
print("Original image:", original_path)
print("Processed image:", processed_path)
print("Original dimensions:", original.size)
print("Processed dimensions:", processed.size)
print("Label:", record["label"])
