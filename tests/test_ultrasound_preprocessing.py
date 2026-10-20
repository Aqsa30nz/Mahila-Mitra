import numpy as np
from PIL import Image

from src.datasets.ultrasound_dataset import load_ultrasound_dataset
from src.preprocessing.ultrasound_preprocessing import (
    IMAGE_SIZE,
    preprocess_image,
    preprocess_record,
)


def test_preprocessed_image_shape_and_range():
    record = load_ultrasound_dataset()[0]
    image = preprocess_image(record["path"])

    assert image.shape == IMAGE_SIZE
    assert image.dtype == np.float32
    assert np.isfinite(image).all()
    assert image.min() >= 0.0
    assert image.max() <= 1.0


def test_preprocess_record_preserves_metadata():
    record = load_ultrasound_dataset()[0]
    processed = preprocess_record(record)

    assert processed["path"] == record["path"]
    assert processed["split"] == record["split"]
    assert processed["label"] == record["label"]
    assert processed["image"].shape == IMAGE_SIZE


def test_custom_image_size(tmp_path):
    image_path = tmp_path / "sample.png"
    Image.new("RGB", (80, 60), color=(128, 64, 255)).save(image_path)

    image = preprocess_image(image_path, image_size=(128, 96))

    assert image.shape == (96, 128)
    assert image.dtype == np.float32
    assert image.min() >= 0.0
    assert image.max() <= 1.0
