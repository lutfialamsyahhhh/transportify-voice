import argparse
from pathlib import Path

import joblib
import numpy as np
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.svm import SVC

from app.asr.constants import DEFAULT_SAMPLE_RATE, TRANSPORT_WORDS
from app.asr.features import extract_dataset_features
from app.config import Config


def train_model(dataset_dir=Config.DATASET_DIR, model_path=Config.ASR_MODEL_PATH):
    labels = TRANSPORT_WORDS
    x, y, metadata = extract_dataset_features(
        dataset_dir=dataset_dir,
        labels=labels,
        sample_rate=DEFAULT_SAMPLE_RATE,
    )

    if x.size == 0:
        raise RuntimeError(
            "No WAV files found. Add recordings under dataset/<word>/word_1.wav before training."
        )

    encoder = LabelEncoder()
    encoded_y = encoder.fit_transform(y)
    scaler = StandardScaler()
    x_scaled = scaler.fit_transform(x)

    stratify = encoded_y if _can_stratify(encoded_y) else None
    x_train, x_test, y_train, y_test = train_test_split(
        x_scaled,
        encoded_y,
        test_size=0.2,
        random_state=42,
        stratify=stratify,
    )

    model = SVC(kernel="rbf", C=10.0, gamma="scale", probability=True, random_state=42)
    model.fit(x_train, y_train)

    y_pred = model.predict(x_test)
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(
        y_test,
        y_pred,
        target_names=encoder.inverse_transform(np.unique(y_test)),
        zero_division=0,
    )

    artifact = {
        "model": model,
        "scaler": scaler,
        "label_encoder": encoder,
        "labels": labels,
        "sample_rate": DEFAULT_SAMPLE_RATE,
        "feature_shape": x.shape[1],
        "accuracy": float(accuracy),
        "classification_report": report,
        "metadata": metadata,
    }

    model_path = Path(model_path)
    model_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(artifact, model_path)

    return artifact


def _can_stratify(encoded_labels):
    _, counts = np.unique(encoded_labels, return_counts=True)
    return len(counts) > 1 and np.min(counts) >= 2


def parse_args():
    parser = argparse.ArgumentParser(description="Train Transportify Voice MFCC + SVM model.")
    parser.add_argument("--dataset", default=str(Config.DATASET_DIR), help="Dataset directory")
    parser.add_argument("--output", default=str(Config.ASR_MODEL_PATH), help="Output joblib path")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    artifact = train_model(dataset_dir=args.dataset, model_path=args.output)
    print(f"Saved ASR model to {args.output}")
    print(f"Accuracy: {artifact['accuracy']:.4f}")
    print(artifact["classification_report"])
