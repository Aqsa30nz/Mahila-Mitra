
from pathlib import Path

import pandas as pd
import torch
from PIL import Image
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms


PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROCESSED_DIR = (
    PROJECT_ROOT / "data" / "processed" / "ultrasound" / "pcosgen"
)

IMAGE_TRANSFORM = transforms.ToTensor()


class PCOSGenDataset(Dataset):
    """Load preprocessed PCOSGen images and binary appearance labels."""

    def __init__(self, csv_path, transform=None):
        self.csv_path = Path(csv_path)
        self.records = pd.read_csv(self.csv_path)
        self.transform = transform or IMAGE_TRANSFORM

        required_columns = {"processed_path", "label"}
        missing = required_columns - set(self.records.columns)

        if missing:
            raise ValueError(
                f"Missing required CSV columns: {sorted(missing)}"
            )

        if self.records.empty:
            raise ValueError(f"No records found in {self.csv_path}")

        self.records["label"] = self.records["label"].astype(int)

        if not set(self.records["label"].unique()).issubset({0, 1}):
            raise ValueError("Labels must be binary: 0 or 1")

        missing_images = [
            path
            for path in self.records["processed_path"]
            if not Path(path).is_file()
        ]

        if missing_images:
            raise FileNotFoundError(
                f"{len(missing_images)} processed images are missing. "
                f"Example: {missing_images[0]}"
            )

    def __len__(self):
        return len(self.records)

    def __getitem__(self, index):
        row = self.records.iloc[index]
        image_path = Path(row["processed_path"])

        with Image.open(image_path) as image:
            image = image.convert("L")
            image = self.transform(image)

        label = torch.tensor(float(row["label"]), dtype=torch.float32)

        return image, label


def create_pcosgen_dataloaders(batch_size=32, num_workers=0):
    """Create DataLoaders using saved preprocessed PNG images."""

    train_dataset = PCOSGenDataset(
        PROCESSED_DIR / "train_preprocessed.csv"
    )
    validation_dataset = PCOSGenDataset(
        PROCESSED_DIR / "validation_preprocessed.csv"
    )

    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=num_workers,
    )

    validation_loader = DataLoader(
        validation_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
    )

    return train_loader, validation_loader
