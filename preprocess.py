import argparse
from pathlib import Path

from scipy.io import wavfile

from app.asr.constants import DEFAULT_SAMPLE_RATE, TRANSPORT_WORDS
from app.config import Config


EXPECTED_RECORDINGS_PER_WORD = 20
MIN_DURATION_SECONDS = 1.0
MAX_DURATION_SECONDS = 2.0


def scan_dataset_structure(dataset_dir=Config.DATASET_DIR, labels=None):
    labels = labels or TRANSPORT_WORDS
    dataset_path = Path(dataset_dir)
    summary = {
        "dataset_dir": str(dataset_path),
        "expected_total": len(labels) * EXPECTED_RECORDINGS_PER_WORD,
        "actual_total": 0,
        "classes": {},
    }

    for label in labels:
        class_dir = dataset_path / label
        files = sorted(class_dir.glob("*.wav")) if class_dir.exists() else []
        class_info = {
            "path": str(class_dir),
            "count": len(files),
            "expected": EXPECTED_RECORDINGS_PER_WORD,
            "complete": len(files) >= EXPECTED_RECORDINGS_PER_WORD,
            "files": [],
        }

        for audio_file in files:
            class_info["files"].append(validate_wav_file(audio_file))

        summary["actual_total"] += len(files)
        summary["classes"][label] = class_info

    return summary


def validate_wav_file(audio_file):
    try:
        sample_rate, data = wavfile.read(audio_file)
        duration = len(data) / float(sample_rate)
        mono = len(getattr(data, "shape", [])) == 1
        valid = (
            sample_rate == DEFAULT_SAMPLE_RATE
            and mono
            and MIN_DURATION_SECONDS <= duration <= MAX_DURATION_SECONDS
        )
        return {
            "path": str(audio_file),
            "sample_rate": int(sample_rate),
            "duration_seconds": round(duration, 3),
            "mono": mono,
            "valid": valid,
        }
    except Exception as exc:
        return {"path": str(audio_file), "valid": False, "error": str(exc)}


def parse_args():
    parser = argparse.ArgumentParser(description="Validate Transportify Voice dataset layout.")
    parser.add_argument("--dataset", default=str(Config.DATASET_DIR), help="Dataset directory")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    dataset_summary = scan_dataset_structure(args.dataset)
    print(f"Dataset: {dataset_summary['dataset_dir']}")
    print(f"Total WAV files: {dataset_summary['actual_total']} / {dataset_summary['expected_total']}")
    for label, info in dataset_summary["classes"].items():
        state = "complete" if info["complete"] else "pending"
        print(f"- {label}: {info['count']} / {info['expected']} ({state})")
