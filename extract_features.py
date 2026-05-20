import argparse
from pathlib import Path

import joblib

from app.asr.constants import DEFAULT_SAMPLE_RATE, TRANSPORT_WORDS
from app.asr.features import extract_dataset_features
from app.config import Config


def export_features(dataset_dir=Config.DATASET_DIR, output_path="features.joblib"):
    x, y, metadata = extract_dataset_features(
        dataset_dir=dataset_dir,
        labels=TRANSPORT_WORDS,
        sample_rate=DEFAULT_SAMPLE_RATE,
    )
    payload = {
        "features": x,
        "labels": y,
        "metadata": metadata,
        "sample_rate": DEFAULT_SAMPLE_RATE,
        "words": TRANSPORT_WORDS,
    }
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(payload, output_path)
    return payload


def parse_args():
    parser = argparse.ArgumentParser(description="Extract MFCC features for Transportify Voice.")
    parser.add_argument("--dataset", default=str(Config.DATASET_DIR), help="Dataset directory")
    parser.add_argument("--output", default="features.joblib", help="Output joblib path")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    exported = export_features(dataset_dir=args.dataset, output_path=args.output)
    print(f"Saved features to {args.output}")
    print(f"Feature matrix: {exported['features'].shape}")
