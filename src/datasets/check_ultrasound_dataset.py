from pathlib import Path
from PIL import Image

root = Path("data/raw/ultrasound/data")
extensions = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

total = 0
empty = []
unreadable = []

for folder in sorted(root.rglob("*")):
    if not folder.is_dir():
        continue

    images = [
        p for p in folder.iterdir()
        if p.is_file() and p.suffix.lower() in extensions
    ]

    if images:
        print(f"{folder}: {len(images)} files")

    for path in images:
        total += 1

        if path.stat().st_size == 0:
            empty.append(path)
            continue

        try:
            with Image.open(path) as img:
                img.verify()
        except Exception as error:
            unreadable.append((path, str(error)))

print(f"\nTotal image files: {total}")
print(f"Empty files: {len(empty)}")
print(f"Unreadable non-empty files: {len(unreadable)}")

for path in empty:
    print("EMPTY:", path)

for path, error in unreadable:
    print("UNREADABLE:", path, "|", error)
