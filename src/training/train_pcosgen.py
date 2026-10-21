from pathlib import Path
import json
import random
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

import numpy as np
import torch
import timm
import torch.nn as nn

from src.datasets.pcosgen_torch_dataset import create_pcosgen_dataloaders
from src.training.pcosgen_engine import train_model


# Reproducibility
SEED = 42
random.seed(SEED)
np.random.seed(SEED)
torch.manual_seed(SEED)

if torch.cuda.is_available():
    torch.cuda.manual_seed_all(SEED)

# Configuration
BATCH_SIZE = 8
EPOCHS = 1
LEARNING_RATE = 0.001
MODEL_NAME = "mobilenetv3_small_100"

PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = PROJECT_ROOT / "outputs" / "pcosgen"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def main():
    print("Device:", DEVICE)
    print("Model:", MODEL_NAME)
    print("Pretrained weights: disabled; random initialization")
    print("Batch size:", BATCH_SIZE)
    print("Pilot epochs:", EPOCHS)

    train_loader, validation_loader = create_pcosgen_dataloaders(
        batch_size=BATCH_SIZE,
        num_workers=0,
    )

    print("Training images:", len(train_loader.dataset))
    print("Validation images:", len(validation_loader.dataset))

    model = timm.create_model(
        MODEL_NAME,
        pretrained=False,
        in_chans=1,
        num_classes=1,
    )

    model = model.to(DEVICE)

    loss_fn = nn.BCEWithLogitsLoss()
    optimizer = torch.optim.SGD(
        model.parameters(),
        lr=LEARNING_RATE,
    )

    results = train_model(
        model=model,
        train_loader=train_loader,
        validation_loader=validation_loader,
        optimizer=optimizer,
        loss_fn=loss_fn,
        epochs=EPOCHS,
        device=DEVICE,
    )

    results_path = OUTPUT_DIR / "mobilenetv3_small_pilot_results.json"
    with results_path.open("w", encoding="utf-8") as file:
        json.dump(results, file, indent=2)

    checkpoint_path = OUTPUT_DIR / "mobilenetv3_small_pilot.pth"
    torch.save(
        {
            "model_name": MODEL_NAME,
            "model_state_dict": model.state_dict(),
            "seed": SEED,
            "batch_size": BATCH_SIZE,
            "learning_rate": LEARNING_RATE,
            "epochs_completed": EPOCHS,
            "results": results,
            "label_definition": (
                "0 = appears normal; 1 = appears abnormal. "
                "These labels do not establish a clinical PCOS diagnosis."
            ),
        },
        checkpoint_path,
    )

    print("\nPilot completed.")
    print("Results saved to:", results_path)
    print("Checkpoint saved to:", checkpoint_path)


if __name__ == "__main__":
    main()
