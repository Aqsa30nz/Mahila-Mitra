from pathlib import Path

import numpy as np
from PIL import Image, ImageOps

IMAGE_SIZE = (224, 224)


def preprocess_image(image_path, image_size=IMAGE_SIZE):
    """Convert an image to grayscale, resize it, and normalize pixels to [0, 1]."""
    image_path = Path(image_path)

    with Image.open(image_path) as image:
        image = ImageOps.exif_transpose(image)
        image = image.convert("L")
        image = image.resize(image_size, Image.Resampling.LANCZOS)

        array = np.asarray(image, dtype=np.float32) / 255.0

    return array


def preprocess_record(record, image_size=IMAGE_SIZE):
    """Preprocess one dataset record while retaining its metadata."""
    array = preprocess_image(record["path"], image_size)

    return {
        "image": array,
        "split": record["split"],
        "label": record["label"],
        "path": record["path"],
    }
