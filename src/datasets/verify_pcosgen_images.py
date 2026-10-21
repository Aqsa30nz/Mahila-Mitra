
from pathlib import Path
from PIL import Image

image_dir = Path("data/processed/ultrasound/pcosgen/images")
files = list(image_dir.glob("*.png"))

bad = []
wrong_dimensions = []
modes = {}

for file in files:
    try:
        with Image.open(file) as image:
            if image.size != (224, 224):
                wrong_dimensions.append((file.name, image.size))

            modes[image.mode] = modes.get(image.mode, 0) + 1
            image.verify()

    except Exception as error:
        bad.append((file.name, str(error)))

print("PNG count:", len(files))
print("Image modes:", modes)
print("Wrong dimensions:", len(wrong_dimensions))
print("Unreadable images:", len(bad))

if wrong_dimensions:
    print("Dimension examples:", wrong_dimensions[:3])

if bad:
    print("Unreadable examples:", bad[:3])

if not files or wrong_dimensions or bad:
    raise SystemExit(1)
