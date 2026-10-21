from PIL import Image

from src.datasets.ultrasound_dataset import load_ultrasound_dataset


def create_sample_dataset(root):
    """Create a small ultrasound dataset for testing."""
    for split in ("train", "test"):
        for label in ("infected", "notinfected"):
            folder = root / split / label
            folder.mkdir(parents=True, exist_ok=True)

            image_path = folder / "sample.png"
            Image.new("RGB", (16, 16), color=(128, 64, 255)).save(image_path)

    # An empty image should be skipped by the loader.
    empty_file = root / "train" / "infected" / "empty.png"
    empty_file.write_bytes(b"")


def test_loader_returns_records(tmp_path):
    create_sample_dataset(tmp_path)

    records = load_ultrasound_dataset(root=tmp_path)

    assert len(records) == 4
    assert all(record["path"].is_file() for record in records)


def test_loader_preserves_train_test_split(tmp_path):
    create_sample_dataset(tmp_path)

    records = load_ultrasound_dataset(root=tmp_path)

    assert {record["split"] for record in records} == {"train", "test"}

    for record in records:
        assert record["path"].parts[-3] == record["split"]


def test_loader_skips_empty_files(tmp_path):
    create_sample_dataset(tmp_path)

    records = load_ultrasound_dataset(root=tmp_path)

    assert len(records) == 4
    assert all(record["path"].stat().st_size > 0 for record in records)


def test_loader_uses_folder_names_as_labels(tmp_path):
    create_sample_dataset(tmp_path)

    records = load_ultrasound_dataset(root=tmp_path)

    assert {record["label"] for record in records} == {
        "infected",
        "notinfected",
    }
