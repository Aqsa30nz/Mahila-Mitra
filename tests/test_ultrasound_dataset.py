from pathlib import Path

from src.datasets.ultrasound_dataset import load_ultrasound_dataset


def test_loader_returns_records():
    records = load_ultrasound_dataset()

    assert len(records) == 3846
    assert all(record["path"].is_file() for record in records)


def test_loader_preserves_train_test_split():
    records = load_ultrasound_dataset()

    assert {record["split"] for record in records} == {"train", "test"}

    for record in records:
        assert record["path"].parts[-3] == record["split"]


def test_loader_skips_empty_files():
    records = load_ultrasound_dataset()

    assert all(record["path"].stat().st_size > 0 for record in records)


def test_loader_uses_folder_names_as_labels():
    records = load_ultrasound_dataset()

    assert {record["label"] for record in records} == {
        "infected",
        "notinfected",
    }

