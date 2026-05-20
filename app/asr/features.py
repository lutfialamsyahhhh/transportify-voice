from pathlib import Path

import librosa
import numpy as np

from app.asr.audio import load_audio
from app.asr.constants import DEFAULT_AUDIO_DURATION_SECONDS, DEFAULT_SAMPLE_RATE, N_MFCC


def extract_features_from_signal(signal, sample_rate=DEFAULT_SAMPLE_RATE, n_mfcc=N_MFCC):
    mfcc = librosa.feature.mfcc(y=signal, sr=sample_rate, n_mfcc=n_mfcc)
    delta = librosa.feature.delta(mfcc)
    delta2 = librosa.feature.delta(mfcc, order=2)
    stacked = np.concatenate([mfcc, delta, delta2], axis=0)

    feature_vector = np.concatenate(
        [
            np.mean(stacked, axis=1),
            np.std(stacked, axis=1),
            np.min(stacked, axis=1),
            np.max(stacked, axis=1),
        ]
    )
    return np.nan_to_num(feature_vector).astype(np.float32), mfcc


def extract_feature_vector(
    audio_path,
    sample_rate=DEFAULT_SAMPLE_RATE,
    duration_seconds=DEFAULT_AUDIO_DURATION_SECONDS,
):
    signal, sr = load_audio(audio_path, sample_rate=sample_rate, duration_seconds=duration_seconds)
    feature_vector, mfcc = extract_features_from_signal(signal, sample_rate=sr)
    return feature_vector, mfcc, signal, sr


def extract_dataset_features(dataset_dir, labels, sample_rate=DEFAULT_SAMPLE_RATE):
    features = []
    targets = []
    metadata = []
    dataset_path = Path(dataset_dir)

    for label in labels:
        class_dir = dataset_path / label
        if not class_dir.exists():
            continue

        for audio_file in sorted(class_dir.glob("*.wav")):
            try:
                feature_vector, _, _, _ = extract_feature_vector(
                    audio_file,
                    sample_rate=sample_rate,
                    duration_seconds=DEFAULT_AUDIO_DURATION_SECONDS,
                )
                features.append(feature_vector)
                targets.append(label)
                metadata.append({"path": str(audio_file), "label": label})
            except Exception as exc:
                metadata.append(
                    {
                        "path": str(audio_file),
                        "label": label,
                        "error": str(exc),
                    }
                )

    if not features:
        return np.empty((0, N_MFCC * 3 * 4), dtype=np.float32), np.array([]), metadata

    return np.vstack(features), np.array(targets), metadata
