
import torch
from sklearn.metrics import (
    balanced_accuracy_score,
    confusion_matrix,
    recall_score,
)


def train_step(model, dataloader, loss_fn, optimizer, device):
    model.train()

    total_loss = 0.0
    total_correct = 0
    total_samples = 0

    for images, labels in dataloader:
        images = images.to(device)
        labels = labels.to(device)

        optimizer.zero_grad()
        logits = model(images).reshape(-1)
        loss = loss_fn(logits, labels)

        loss.backward()
        optimizer.step()

        predictions = (torch.sigmoid(logits) >= 0.5).float()
        batch_size = labels.size(0)

        total_loss += loss.item() * batch_size
        total_correct += (predictions == labels).sum().item()
        total_samples += batch_size

    return {
        "loss": total_loss / total_samples,
        "accuracy": total_correct / total_samples,
    }


@torch.no_grad()
def validation_step(model, dataloader, loss_fn, device):
    model.eval()

    total_loss = 0.0
    total_samples = 0
    all_labels = []
    all_predictions = []

    for images, labels in dataloader:
        images = images.to(device)
        labels = labels.to(device)

        logits = model(images).reshape(-1)
        loss = loss_fn(logits, labels)

        predictions = (torch.sigmoid(logits) >= 0.5).long()

        batch_size = labels.size(0)
        total_loss += loss.item() * batch_size
        total_samples += batch_size

        all_labels.extend(labels.long().cpu().tolist())
        all_predictions.extend(predictions.cpu().tolist())

    matrix = confusion_matrix(
        all_labels, all_predictions, labels=[0, 1]
    )

    return {
        "loss": total_loss / total_samples,
        "accuracy": sum(
            actual == predicted
            for actual, predicted in zip(all_labels, all_predictions)
        ) / total_samples,
        "balanced_accuracy": balanced_accuracy_score(
            all_labels, all_predictions
        ),
        "normal_recall": recall_score(
            all_labels, all_predictions, pos_label=0, zero_division=0
        ),
        "abnormal_recall": recall_score(
            all_labels, all_predictions, pos_label=1, zero_division=0
        ),
        "confusion_matrix": matrix.tolist(),
    }


def train_model(
    model,
    train_loader,
    validation_loader,
    optimizer,
    loss_fn,
    epochs=1,
    device="cpu",
):
    results = {
        "train_loss": [],
        "train_acc": [],
        "validation_loss": [],
        "validation_acc": [],
        "validation_balanced_accuracy": [],
        "validation_normal_recall": [],
        "validation_abnormal_recall": [],
        "validation_confusion_matrix": [],
    }

    model.to(device)

    for epoch in range(epochs):
        train_metrics = train_step(
            model, train_loader, loss_fn, optimizer, device
        )
        validation_metrics = validation_step(
            model, validation_loader, loss_fn, device
        )

        results["train_loss"].append(train_metrics["loss"])
        results["train_acc"].append(train_metrics["accuracy"])
        results["validation_loss"].append(validation_metrics["loss"])
        results["validation_acc"].append(validation_metrics["accuracy"])
        results["validation_balanced_accuracy"].append(
            validation_metrics["balanced_accuracy"]
        )
        results["validation_normal_recall"].append(
            validation_metrics["normal_recall"]
        )
        results["validation_abnormal_recall"].append(
            validation_metrics["abnormal_recall"]
        )
        results["validation_confusion_matrix"].append(
            validation_metrics["confusion_matrix"]
        )

        print(
            f"Epoch {epoch + 1}/{epochs} | "
            f"Train loss: {train_metrics['loss']:.4f} | "
            f"Train accuracy: {train_metrics['accuracy']:.4f} | "
            f"Validation loss: {validation_metrics['loss']:.4f} | "
            f"Validation accuracy: {validation_metrics['accuracy']:.4f} | "
            f"Balanced accuracy: "
            f"{validation_metrics['balanced_accuracy']:.4f} | "
            f"Normal recall: {validation_metrics['normal_recall']:.4f} | "
            f"Abnormal recall: {validation_metrics['abnormal_recall']:.4f}"
        )
        print(
            "Confusion matrix [[TN, FP], [FN, TP]]:",
            validation_metrics["confusion_matrix"],
        )

    return results
